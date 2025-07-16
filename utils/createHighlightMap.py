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


# --- Final output ---
insertion_sort()
print(highlight_map)