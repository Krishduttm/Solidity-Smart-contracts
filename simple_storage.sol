// SPDX-License-Identifier: MIT

pragma solidity >=0.6.0;

contract simple_storage {
    uint256 public favnum;

    function store(uint256 _favnum) public {
        favnum = _favnum;
    }

    function retrieve() public view returns (uint256) {
        return favnum + favnum;
    }

    struct People {
        uint256 Favnum;
        string name;
    }
    People[] public people;

    mapping(string => uint256) public Favnumfinder;

    function AddPeople(uint256 _favnum, string memory _name) public {
        people.push(People(_favnum, _name));

        Favnumfinder[_name] = _favnum;
    }

    function SeePeople(string memory str) public view returns (uint256) {
        return Favnumfinder[str];
    }
}
