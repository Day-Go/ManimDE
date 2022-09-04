def bubble_sort(data):
    swapped = False
    for n in range(len(data)-1, 0, -1):
        for i in range(n):
            if data[i] > data[i+1]:
                swapped = True
                data[i], data[i+1] = data[i+1], data[i]

        if not swapped:
            return

def insertion_sort(data) -> None:
    for step in range(1, len(data)):
        key = data[step]
        j = step - 1

        while j >= 0 and data[j] > key:
            data[j + 1] = data[j]
            j = j - 1
            
        data[j + 1] = key