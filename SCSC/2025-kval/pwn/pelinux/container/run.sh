#!/bin/bash
qemu-system-x86_64 -kernel bzImage -initrd initramfs.cpio -nographic -append "console=ttyS0" -monitor none $@