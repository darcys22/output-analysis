#!/bin/bash

/home/sean/oxen-core/build/bin/oxen-wallet-cli --daemon-address public.loki.foundation:38157 --testnet --wallet-file ~/sdloki/test --password "password" unspent_outputs > data/wallet-outputs.txt
