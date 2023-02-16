const Web3 = require('web3')
// const ABI = require('./abi.json')
// import ABI from './abi.json';
const fs = require('fs');
const abiDecoder = require('abi-decoder');

const web3 = new Web3('wss://young-little-brook.bsc-testnet.discover.quiknode.pro/');
const abi = JSON.parse(fs.readFileSync('abi_market.json'))

const COLLECTION = 'NVCM.Collection';
const NFT = "NVCM.Nft";
const LISTING = "NVCM.Listing";
const NFTEVENT = "NVCM.NftEvent";
count = 0;
abiDecoder.addABI(abi);
async function appendToFile(fileName, data) {
    // console.log(data['topics'])
    console.log(data['transactionHash']);
    // web3.eth.waitForTransactionReceipt(data['transactionHash']);
    let tx = await web3.eth.getTransaction(data['transactionHash']);
    console.log(tx)
    let info = abiDecoder.decodeMethod(tx['input'])
    console.log(info)
    fs.appendFile(fileName, JSON.stringify(data) + '\n', function (err) {
        if (err) throw err;
        console.log(`Saved to ${fileName} | ${++count}`);
    });
}
//list:0xd547e933094f12a9159076970143ebe73234e64480317844b0dcb36117116de4
//update:0xd547e933094f12a9159076970143ebe73234e64480317844b0dcb36117116de4
//delist:0x9ba1a3cb55ce8d63d072a886f94d2a744f50cddf82128e897d0661f5ec623158
//buy:0x263223b1dd81e51054a4e6f791d45a4a1ddb4aadcd93a2dfd892615c3fdac187
//transfer:0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef
let options = {
    fromBlock: 'latest',
    address: [
        '0x408D5094271E6Bb288bb48375104dDe27E34D6f0',
        '0x247D6B56f4f1960e9A761cb1A321d77eCa89F2B5',


    ],    //Only get events from specific addresses
    topics: []                              //What topics to subscribe to
};

let subscription = new web3.eth.subscribe('logs', options, (err, event) => {
    if (!err)
        return;
    // console.log(event)
});


// function listEvent(TokenId, CollectionId, Active, Price, Seller, DateTime) {
//     let tx = await web3.eth.getTransaction(data['transactionHash']);
//     console.log(tx)
//     let info = abiDecoder.decodeMethod(tx['input'])
//     let addingEvent = new String(`INSERT INTO ${NFTEVENT} (TokenId,CollectionId,EventName,From,To,DateTime) VALUES (${TokenId},${CollectionId},${EventName},0,0,${DateTime})`)

// }



subscription.on('data', async (event) => await appendToFile('./data/data.txt', event))
    .on('changed', changed => appendToFile('./data/changed.txt', changed))
    .on('error', err => appendToFile('./data/error.txt', { message: err.message, stack: err.stack }))
    .on('connected', str => console.log('connected'))