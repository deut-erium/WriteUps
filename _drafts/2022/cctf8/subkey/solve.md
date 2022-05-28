`curl https://getsubstrate.io -sSf | bash -s -- --fast`  
`cargo install --force subkey --git https://github.com/paritytech/substrate --version 2.0.1 --locked`  
`cargo build -p subkey --release`  

```
~/.cargo/bin/subkey inspect 0x4ead8340dfcdb3a86bdf34b09e98db53a09d8f050
804f3ab2cee40edaf875cac
Secret Key URI `0x4ead8340dfcdb3a86bdf34b09e98db53a09d8f050804f3ab2cee40edaf875cac` is account:
  Network ID:        substrate
 Secret seed:       0x4ead8340dfcdb3a86bdf34b09e98db53a09d8f050804f3ab2cee40edaf875cac
  Public key (hex):  0xbe2b683e2264b7ba20a80d00e065b5be09d6495d64b7a5d204606d83c4bbc557
  Account ID:        0xbe2b683e2264b7ba20a80d00e065b5be09d6495d64b7a5d204606d83c4bbc557
  Public key (SS58): 5GN3rFGWqHwys6k3yHyZ5sciRgBGoQzeT7CNREcXQpSFKedE
  SS58 Address:      5GN3rFGWqHwys6k3yHyZ5sciRgBGoQzeT7CNREcXQpSFKedE
```

flag = CCTF{0xbe2b683e2264b7ba20a80d00e065b5be09d6495d64b7a5d204606d83c4bbc557}
