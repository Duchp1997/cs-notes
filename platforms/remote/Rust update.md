## 使用中科大源更新Rust

```bash
# edit .bashrc file
$ vim ~/.bashrc
# add the following two lines to .bachrc
export RUSTUP_DIST_SERVER=https://mirrors.ustc.edu.cn/rust-static
export RUSTUP_UPDATE_ROOT=https://mirrors.ustc.edu.cn/rust-static/rustup

# update now
$ source ~/.bashrc
```

