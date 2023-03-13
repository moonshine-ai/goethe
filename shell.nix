{ pkgs ? import <nixpkgs> { } }:

let python-packages = p: with p; [ sentencepiece torch 
(buildPythonPackage rec {
 pname = "fairscale";
 version = "0.4.13";
 src = fetchPypi {
	 inherit pname version;
	 sha256 = "G3l4JcQn9dupIlP9DY2qV06L1lGiQjSXd1+rGzDPt2g=";
 };
 doCheck = false;
 propagatedBuildInputs = with pkgs.python3Packages; [
 numpy
 torch
 ];
 })
];
in pkgs.mkShell {
	nativeBuildInputs = [ (pkgs.python3.withPackages python-packages) ];
}
