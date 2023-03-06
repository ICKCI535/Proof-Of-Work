async function main() {
    const Web3 = require('web3');
    const web3 = new Web3('https://goerli.infura.io/v3/5d290665663443a98c4f32f990e491c5');
    const abiDecoder = require('abi-decoder');
    var fs = require('fs');
    const abi = JSON.parse(fs.readFileSync('D://Betting//scripts//abi.json', 'utf-8'))
    let txrecepit = await web3.eth.getTransactionReceipt('0x868e978d3e66a13fe058408cdfda4cc499072918dec102cfe042430b0730b886');
    abiDecoder.addABI(abi);
    var log = abiDecoder.decodeLogs(txrecepit.logs);
    console.log(log[0].events);
}
main()