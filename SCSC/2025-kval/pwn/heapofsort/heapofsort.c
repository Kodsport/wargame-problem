#include <stdio.h>
#include <stdlib.h>

typedef long long sizetype;

typedef struct heap {
    sizetype arr[100];
    sizetype size;
    void (*heapify)(struct heap *h, sizetype idx);
    void (*adjust)(struct heap *h, sizetype idx);
    void (*swap)(struct heap *h, sizetype idx);
    void (*insert)(struct heap *h, sizetype key);
    void (*remove)(struct heap *h, sizetype idx);
    void (*print)(struct heap *h);
} heap_t;

void heap_swap(heap_t *h, sizetype idx) {
    sizetype pidx = (idx-1)/2;
    sizetype cv = h->arr[idx];
    sizetype pv = h->arr[pidx];
    h->arr[idx] = pv;
    h->arr[pidx] = cv;
}

void heap_heapify(heap_t *h, sizetype idx) {
    sizetype root = idx;
    sizetype left = 2 * root + 1;
    sizetype right = 2 * root + 2;

    if (h->size < left && h->arr[left] > h->arr[root]) {
        root = left;
    }

    if (h->size < right && h->arr[right] > h->arr[root]) {
        root = right;
    }

    if (root != idx) {
        h->swap(h, root);
        h->heapify(h, root);
    }
}

void heap_adjust(heap_t *h, sizetype idx) {
    int pidx = (idx - 1) / 2;
    if (pidx >= 0 && h->arr[idx] > h->arr[pidx]) {
        h->swap(h, idx);
        h->adjust(h, pidx);
    }
}

void heap_insert(heap_t *h, sizetype v) {
    h->arr[++h->size - 1] = v;
    h->adjust(h, h->size-1);
    h->heapify(h, 0);
}

void heap_remove(heap_t *h, sizetype idx) {
    h->arr[idx] = (unsigned long long)-1;
    h->adjust(h, 0);
    h->arr[0] = h->arr[--h->size];
    h->heapify(h, 0);
}

void heap_print(heap_t *h) {
    printf("Heap: ");
    for (sizetype i = 0; i < h->size; i++) {
        printf("%lld ", h->arr[i]);
    }
    puts("");
}

heap_t new_heap() {
    static heap_t h = {
        .arr = {0},
        .size = 0,
        .heapify = heap_heapify,
        .adjust = heap_adjust,
        .swap = heap_swap,
        .insert = heap_insert,
        .remove = heap_remove,
        .print = heap_print
    };

    return h;
}

sizetype get_num() {
    char buf[16] = {0};
    fgets(buf, 16, stdin);
    return strtoll(buf, NULL, 10);
}

int menu() {
    puts("1. Insert value");
    puts("2. Remove index");
    puts("3. Print Heap");
    printf("Option: ");
    return get_num();
}

int main() {
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stdin, NULL, _IONBF, 0);

    heap_t heap = new_heap();

    while (1) {
        switch (menu()) {
            case 1:
                printf("Value: ");
                heap.insert(&heap, get_num());
                break;
            case 2:
                printf("Index: ");
                heap.remove(&heap, get_num());
                break;
            case 3:
                heap.print(&heap);
                break;
        }
    }
}