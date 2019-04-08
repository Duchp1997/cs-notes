# Git LFS

Setup Git LFS for new repository:

```shell
$ git lfs install
```

Track specific file or file type:

```shell
$ git lfs track "*.iso"
```

Commit as usual:

```shell
$ git add file.iso
$ git commit -m "Add disk image"
$ git push
```

