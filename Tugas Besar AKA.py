import time 
import matplotlib.pyplot as plt 
from prettytable import PrettyTable 
import requests 
import cProfile 

def bacaData(linkGithub, num_data):
    try:
        response = requests.get(linkGithub)
        response.raise_for_status()

        data = response.text.strip().split(';')

        dataBersih = []

        for item in data:
            try:
                cleaned_item = item.strip() 
                if cleaned_item:
                    dataBersih.append(float(cleaned_item)) 
            except ValueError:
                continue 

        return dataBersih[:num_data] 

    except requests.RequestException as e:
        print(f"Error mengambil data dari GitHub: {e}")
        return []

def mergeShortIteratif(arr):
    def merge(arr, left, mid, right):
        left_half = arr[left:mid+1]
        right_half = arr[mid+1:right+1]

        i = j = 0
        k = left

        while i < len(left_half) and j < len(right_half):
            if left_half[i] <= right_half[j]:
                arr[k] = left_half[i]
                i += 1
            else:
                arr[k] = right_half[j]
                j += 1
            k += 1

        while i < len(left_half):
            arr[k] = left_half[i]
            i += 1
            k += 1

        while j < len(right_half):
            arr[k] = right_half[j]
            j += 1
            k += 1

    n = len(arr)
    curr_size = 1

    while curr_size < n:
        for start in range(0, n, 2*curr_size):
            mid = start + curr_size - 1
            end = min(start + 2*curr_size - 1, n - 1)

            merge(arr, start, mid, end)

        curr_size *= 2

    return arr

def mergeShortRekursif(arr):
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left = mergeShortRekursif(arr[:mid])
    right = mergeShortRekursif(arr[mid:])

    return merge_recursive(left, right)

def merge_recursive(left, right):
    result = []
    i = j = 0

    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])

    return result

def profile_sorting_algorithm(func, data):
    profiler = cProfile.Profile()
    profiler.enable()

    start_time = time.time()
    func(data.copy())
    end_time = time.time()

    profiler.disable()

    return end_time - start_time

def update_graph(n_values, iterative_times, recursive_times):
    plt.figure(figsize=(12, 6))
    plt.subplot(1, 2, 1)
    plt.plot(n_values, iterative_times, label='Iterative', marker='o')
    plt.plot(n_values, recursive_times, label='Recursive', marker='x')
    plt.title('Merge Sort: Execution Time')
    plt.xlabel('Input Size')
    plt.ylabel('Time (seconds)')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def print_performance_table(n_values, iterative_times, recursive_times):
    table = PrettyTable()
    table.field_names = [
        "Input Size",
        "Iterative Time (detik)",
        "Recursive Time (detik)",
        "Selisih"
    ]

    for n, iter_time, rec_time in zip(n_values, iterative_times, recursive_times):
        table.add_row([
            n,
            f"{iter_time:.6f}",
            f"{rec_time:.6f}",
            f"{abs(iter_time - rec_time):.6f}"
        ])

    print(table)

def main():
    # URL RAW file dari GitHub
    linkGithub = 'https://raw.githubusercontent.com/AdithanaDharma/Iterative-vs-Recursive-Merge-Sort-for-Rating-on-MyAnimeList-Website/refs/heads/main/Data%20Rating%20MAL.txt'

    n_values = []
    iterative_times = []
    recursive_times = []

    n = 1
    while n <= 4440:
        try:
            # Baca data
            data = bacaData(linkGithub, n)

            if not data:
                print("Gagal membaca data.")
                break

            # Profiling dan ukur waktu
            iterative_time = profile_sorting_algorithm(
                mergeShortIteratif,
                data
            )

            recursive_time = profile_sorting_algorithm(
                mergeShortRekursif,
                data
            )

            # Tambahkan ke daftar
            n_values.append(n)
            iterative_times.append(iterative_time)
            recursive_times.append(recursive_time)

            # Cetak tabel performa
            print_performance_table(
                n_values,
                iterative_times,
                recursive_times
            )

            # Update grafik
            update_graph(
                n_values,
                iterative_times,
                recursive_times
            )

            # Naikkan ukuran input
            n += 1100

        except Exception as e:
            print(f"Terjadi kesalahan: {e}")
            break

if __name__ == "__main__":
    main()
