// Irrelevant to the challenge
class Queue {
  constructor(maxConcurrent, maxQueueSize) {
    this.queue = [];
    this.running = 0;
    this.maxConcurrent = maxConcurrent;
    this.maxQueueSize = maxQueueSize;
  }

  async add(task, timeout) {
    if (this.queue.length >= this.maxQueueSize) {
      throw new Error("Queue is full");
    }

    return new Promise((resolve, reject) => {
      const timeoutId = setTimeout(() => {
        const index = this.queue.findIndex(
          (item) => item.timeoutId === timeoutId
        );
        if (index > -1) {
          this.queue.splice(index, 1);
          reject(new Error("Request timed out"));
        }
      }, timeout);

      this.queue.push({ task, resolve, reject, timeoutId });
      this.processNext();
    });
  }

  async processNext() {
    if (this.running >= this.maxConcurrent || this.queue.length === 0) {
      return;
    }

    this.running++;
    const { task, resolve, reject, timeoutId } = this.queue.shift();
    clearTimeout(timeoutId);

    try {
      const result = await task();
      resolve(result);
    } catch (error) {
      reject(error);
    } finally {
      this.running--;
      this.processNext();
    }
  }
}

module.exports = Queue;
