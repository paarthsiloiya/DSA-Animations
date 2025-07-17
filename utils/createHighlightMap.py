# generate_highlight_map.py

highlight_map = []
time_elapsed = 0.0

def wait(duration):
    global time_elapsed
    time_elapsed += duration

def play(run_time):
    global time_elapsed
    time_elapsed += run_time

def log(line, label=None):
    entry = {
        "time": round(time_elapsed, 3),
        "lines": str(line),
    }
    if label:
        entry["label"] = label
    highlight_map.append(entry)

# --- Sorting Algo ---
def bubble_sort():
    values = [5, 2, 4, 6, 3, 1]
    n = len(values)

    wait(1)

    for i in range(n):
        log(5, "j loop end")
        for j in range(n - i - 1):
            wait(0.2)
            val1 = values[j]
            val2 = values[j + 1]
            log(6, f"Select elements {val1} and {val2}")
            wait(0.2)
            if val1 > val2:
                wait(1.2)
                log(7, f"Swapping elements {val1} and {val2}")
                wait(0.3)
                values[j], values[j + 1] = values[j + 1], values[j]
                wait(0.2)
            else:
                wait(0.2)
            wait(0.4)
            log(5, "j loop end")
            wait(0.3)
        log(3, f"i loop end")
        wait(0.2)
        log(4, f"swapped=False")
        wait(0.1)

    wait(1)


def insertion_sort():
    arr = [5, 2, 4, 6, 3, 1]
    play(1)  # First .MarkSorted() in Manim
    for i in range(1, len(arr)):
        #play(0.4) # Shift Element Up Split into 0.1, 0.2, 0.1
        play(0.1)
        log(2, f"i = {i}")
        key = arr[i]
        play(0.2)
        log(3, f"key = {key}")
        j = i - 1
        play(0.1)
        log(4, f"j = {j}")
        insert_index = j + 1
        shifted = False
        while j >= 0 and arr[j] > key:
            play(0.2)  # Select Element
            wait(0.3)
            log(5, f"Comparing {arr[j]} > {key}")
            play(0.2)  # Write compare_text
            wait(0.3)
            play(0.3)  # Create(shiftArrow)
            play(0.2)  # Write(shiftText)
            log(6, f"Shifting {arr[j]} to position {j+1}")
            play(0.3)  # shift RIGHT
            play(0.2)  # FadeOuts
            play(0.2)  # ClearSelection
            arr[j + 1] = arr[j]
            log(7, f"Decrement j to {j - 1}")
            j -= 1
            shifted = True
            insert_index = j + 1
        if not shifted:
            wait(0.3)
            log(5, f"Comparing {arr[j]} > {key}")
            wait(0.2)
    
        log(8, f"Inserting {key} at position {insert_index}")
        play(0.4)  # Move to final position
        arr[insert_index] = key
        play(0.15)  # MarkSorted()
        wait(0.2)
    wait(1.0)  # Final hold


def selection_sort():
    arr = [5, 2, 4, 6, 3, 1]
    wait(1)
    for i in range(len(arr)):
        min_idx = i
        log(3, f"i = {i}")
        play(0.3) # Create i and min pointer
        log(4, f"min_idx = {min_idx}")
        for j in range(i + 1, len(arr)):
            wait(0.1)
            log(5, f"j = {j}")
            play(0.2) # Select Element j
            log(6, f"Comparing {arr[j]} < {arr[min_idx]}")
            if arr[j] < arr[min_idx]:
                wait(0.3)
                play(0.2) # Write compare_text
                min_idx = j
                log(7, f"New min_idx = {min_idx}")
                play(0.3) # Update min pointer
                wait(0.2)
            wait(0.2)
            play(0.2) # Clear selection
            wait(0.1)
        
        play(0.2) # Fade out i and min pointer
        if min_idx != i:
            play(0.3) # Create swap arrow
            play(0.4) # Swap Text
            wait(0.2)
            log(8, f"Swapping {arr[i]} and {arr[min_idx]}")
            play(0.3) # Swap elements
            arr[i], arr[min_idx] = arr[min_idx], arr[i]
            wait(0.1)
            play(0.2) # Fade out swap arrow & Text
        else:
            play(0.3) # Create swap arrow
            log(8, f"No swap needed for {arr[i]}")
            play(0.4) # Swap Text
            wait(0.2)
            play(0.2) # Fade out swap arrow & Text
        
        play(0.2) # Mark i as sorted
        wait(0.3)
    wait(1.0)  # Final hold


def quick_sort():
    def swap_delay(arr, i, j, return_line):
        play(0.3) # Create swap arrow
        log(11, f"Function call swap(arr, {i}, {j})")
        play(0.4) # Swap Text
        log(12, f"Swapping {arr[i]} and {arr[j]}")
        play(0.3) # Swap
        arr[i], arr[j] = arr[j], arr[i]
        wait(0.1)
        play(0.2) # Fade out swap arrow & Text
        log(return_line, f"Returning from swap")

    def sort(arr, low, high):
        log(14, f"quick_sort(arr, {low}, {high})")
        wait(0.1)
        log(15, f"if {low} < {high}")
        wait(0.2)
        if low < high:
            log(16, f"partitioning {arr[low:high+1]} from {low} to {high}")
            pi = partition(arr, low, high)
            play(0.2) # Create partition Rectangle
            log(17, f"quick_sort(arr, {low}, {pi - 1})")
            wait(0.1)
            sort(arr, low, pi - 1)
            play(0.3) # Fade out partition Rectangle
            wait(0.2)
            play(0.2) # Create partition Rectangle
            log(18, f"quick_sort(arr, {pi + 1}, {high})")
            wait(0.1)
            sort(arr, pi + 1, high)
            play(0.3) # Fade out partition Rectangle

        else:
            wait(0.4)
            play(0.2) # Mark sorted elements
            wait(0.4)
        
    def partition(arr, low, high):
        log(2, f"pivot = {arr[high]}")
        play(0.2) # Select pivot
        pivot = arr[high]
        wait(0.2)
        log(3, f"i = {low - 1}")
        i = low - 1
        play(0.2) # Create i pointer
        play(0.2) # Create j pointer
        for j in range(low, high):
            log(4, f"j = {j}")
            play(0.3) # Initialize i pointer position
            wait(0.2)
            if arr[j] < pivot:
                log(5, f"Comparing {arr[j]} < {pivot}")
                play(0.3) # Write compare_text
                wait(0.6)
                play(0.2) # Fade out compare_text
                wait(0.2)
                i += 1
                log(6, f"Incrementing i to {i}")
                play(0.3) # Update i pointer position
                log(7, f"Swapping {arr[i]} and {arr[j]}")
                swap_delay(arr, i, j, 7)
                wait(0.1)
            else:
                play(0.3) # Write No Swap Text
                log(5, f"No swap needed for {arr[j]}")
                wait(0.6)
                play(0.2) # Fade out No Swap Text
                wait(0.3)
        
        play(0.2) # Fade out j pointer
        play(0.3) # Write Increment i Text
        wait(0.6)
        play(0.2) # Fade out Increment i Text
        wait(0.1)
        play(0.2) # Increment i pointer
        log(8, f"Swapping pivot {arr[high]} with {arr[i + 1]}")
        swap_delay(arr, i + 1, high, 8)
        wait(0.2)
        play(0.2) # Mark pivot as sorted
        wait(0.2)
        play(0.2) # Fade out i pointer
        play(0.2) # Clear Selection
        log(9, f"Returning partition index {i + 1}")
        wait(0.3)
        log(16, f"End of partition function")
        return i + 1

    arr = [5, 2, 4, 6, 3, 1]
    wait(1)
    sort(arr, 0, len(arr) - 1)
    wait(1.0)  # Final hold

# --- Final output ---
quick_sort()
print(highlight_map)