pragma solidity ^0.8.13;

interface IAmm {
    function maintenanceMarginRatio() external view returns (uint256);
}

interface IClearingHouse {
    function getMarginRatio(IAmm _amm, address _trader) external view returns (int256);
}

contract LiquidationReader {
    // if one target is found, immediately returns
    function getLiquidationTargets(IAmm amm, address[] calldata traders) public view returns (address trader) {
        int256 marginRatio = int256(amm.maintenanceMarginRatio());
        for (uint256 i = 0; i < traders.length; i++) {
            try IClearingHouse(0x01b6407ADf740d135ddF1eBDD1529407845773F3).getMarginRatio(amm, traders[i]) returns (int256 ratio) {
                if(ratio < marginRatio) {
                    return traders[i];
                }
            } catch {
                continue;
            }
        }
    }

    function getLiquidationTargetsInMultipleAmm(IAmm[] calldata amms, address[] calldata traders) external view returns (address amm, address trader) {
        for (uint256 i = 0; i < amms.length; i++) {
            address res = address(getLiquidationTargets(amms[i], traders));
            if (res != address(0)) {
                return (address(amms[i]), res);
            }
        }
    }
}
