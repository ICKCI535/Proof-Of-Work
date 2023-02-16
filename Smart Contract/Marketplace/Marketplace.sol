//SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.7;

import "./extensions/IERC721A.sol";
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

interface IERC20 {
    function transfer(address to, uint256 value) external returns (bool);

    function transferFrom(
        address from,
        address to,
        uint256 value
    ) external returns (bool);

    function balanceOf(address owner) external view returns (uint);
}

// Errors
error PriceNotMet(address nftAddress, uint256 tokenId, uint256 price);
error ItemNotForSale(address nftAddress, uint256 tokenId);
error NotListed(address nftAddress, uint256 tokenId);
error AlreadyListed(address nftAddress, uint256 tokenId);
error NoProceeds();
error NotOwner();
error NotApprovedForMarketplace();
error PriceMustBeAboveMinPrice();

contract Marketplace is Ownable, ReentrancyGuard {
    //Struct
    struct Listing {
        uint256 price;
        address seller;
    }

    //Events
    /**
     *@dev pop up when item is listed
     * @param seller the address of the seller
     * @param nftAddress the address of the nft collection
     * @param tokenId token id of the nft
     * @param price of the nft
     */
    event ItemListed(
        address seller,
        address nftAddress,
        uint256 tokenId,
        uint256 price
    );

    /**
     *@dev pop up when item is updated listing
     * @param seller the address of the seller
     * @param nftAddress the address of the nft collection
     * @param tokenId token id of the nft
     * @param price of the nft
     */
    event ItemUpdateListed(
        address seller,
        address nftAddress,
        uint256 tokenId,
        uint256 price
    );

    /**
     *@dev pop up when item is canceled listing
     * @param seller the address of the seller
     * @param nftAddress the address of the nft collection
     * @param tokenId token id of the nft
     */
    event ItemCanceled(address seller, address nftAddress, uint256 tokenId);

    /**
     *@dev pop up when item is bought
     * @param seller the address of the seller
     * @param buyer the address of the buyer
     * @param nftAddress the address of the nft collection
     * @param tokenId token id of the nft
     * @param price of the nft
     */
    event ItemBought(
        address seller,
        address buyer,
        address nftAddress,
        uint256 tokenId,
        uint256 price
    );
    // State Variables
    mapping(address => mapping(uint256 => Listing)) public s_listings;

    address private ownerAddress = 0xE515BA407b97B053F89c4eecb8886F4C6101d4A3;
    address public constant BUSD_CONTRACT =
        0x78867BbEeF44f2326bF8DDd1941a4439382EF2A7;

    // Function modifiers

    /**
     *@dev require not listed
     * @param nftAddress the address of the nft collection
     * @param tokenId token id of the nft
     * @param owner nft owner
     */
    modifier notListed(address nftAddress, uint256 tokenId) {
        Listing memory listing = s_listings[nftAddress][tokenId];
        if (listing.price > 0) {
            revert AlreadyListed(nftAddress, tokenId);
        }
        _;
    }

    /**
     *@dev require is nft owner
     * @param nftAddress the address of the nft collection
     * @param tokenId token id of the nft
     * @param spender address of user
     */
    modifier isNftOwner(
        address nftAddress,
        uint256 tokenId,
        address spender
    ) {
        address owner = IERC721A(nftAddress).ownerOf(tokenId);
        if (spender != owner) {
            revert NotOwner();
        }
        _;
    }

    /**
     *@dev require nft listed
     * @param nftAddress the address of the nft collection
     * @param tokenId token id of the nft
     */
    modifier isListed(address nftAddress, uint256 tokenId) {
        Listing memory listing = s_listings[nftAddress][tokenId];
        if (listing.price <= 0) {
            revert NotListed(nftAddress, tokenId);
        }
        _;
    }

    // Function

    /**
     *@dev Listing item, require the nft is not listed and is the nft owner
     * @param nftAddress the address of the nft collection
     * @param tokenId token id of the nft
     * @param price of the nft
     */
    function listItem(
        address nftAddress,
        uint256 tokenId,
        uint256 price
    )
        external
        notListed(nftAddress, tokenId, msg.sender)
        isNftOwner(nftAddress, tokenId, msg.sender)
    {
        if (price <= 1000000000000000) {
            revert PriceMustBeAboveMinPrice();
        }

        if (IERC721A(nftAddress).getApproved(tokenId) != address(this)) {
            revert NotApprovedForMarketplace();
        }
        s_listings[nftAddress][tokenId] = Listing(price, msg.sender);
        emit ItemListed(msg.sender, nftAddress, tokenId, price);
    }

    /**
     *@dev Cancel listing item, require the nft is listed and is the nft owner
     * @param nftAddress the address of the nft collection
     * @param tokenId token id of the nft
     */
    function cancelListing(
        address nftAddress,
        uint256 tokenId
    )
        external
        isListed(nftAddress, tokenId)
        isNftOwner(nftAddress, tokenId, msg.sender)
    {
        delete (s_listings[nftAddress][tokenId]);
        emit ItemCanceled(msg.sender, nftAddress, tokenId);
    }

    /**
     *@dev Buy item, require the nft is listed and the listing is active
     * @param nftAddress the address of the nft collection
     * @param tokenId token id of the nft
     */
    function buyItem(
        address nftAddress,
        uint256 tokenId
    ) external isListed(nftAddress, tokenId) nonReentrant {
        //check owner of tokenId

        require(
            IERC721A(nftAddress).ownerOf(tokenId) ==
                s_listings[nftAddress][tokenId].seller
        );

        //check msg.value == price

        Listing memory listedItem = s_listings[nftAddress][tokenId];
        if (IERC20(BUSD_CONTRACT).balanceOf(msg.sender) < listedItem.price) {
            revert PriceNotMet(nftAddress, tokenId, listedItem.price);
        }
        uint256 _reward = (listedItem.price * 90) / 100;
        uint256 _royalty = listedItem.price - _reward;
        IERC721A(nftAddress).safeTransferFrom(
            listedItem.seller,
            msg.sender,
            tokenId
        );
        IERC20(BUSD_CONTRACT).transferFrom(
            msg.sender,
            listedItem.seller,
            _reward
        );
        IERC20(BUSD_CONTRACT).transferFrom(msg.sender, ownerAddress, _royalty);
        delete (s_listings[nftAddress][tokenId]);
        emit ItemBought(
            msg.sender,
            listedItem.seller,
            nftAddress,
            tokenId,
            listedItem.price
        );
    }

    /**
     *@dev Listing item, require the nft is listed and is the nft owner
     * @param nftAddress the address of the nft collection
     * @param tokenId token id of the nft
     * @param newPrice of the nft
     */
    function updateListing(
        address nftAddress,
        uint256 tokenId,
        uint256 newPrice
    )
        external
        isListed(nftAddress, tokenId)
        nonReentrant
        isNftOwner(nftAddress, tokenId, msg.sender)
    {
        if (newPrice <= 1000000000000000) {
            revert PriceMustBeAboveMinPrice();
        }
        s_listings[nftAddress][tokenId].price = newPrice;
        emit ItemUpdateListed(msg.sender, nftAddress, tokenId, newPrice);
    }

    function getListing(
        address nftAddress,
        uint256 tokenId
    ) external view returns (Listing memory) {
        Listing memory listing = s_listings[nftAddress][tokenId];
        return listing;
    }
}
