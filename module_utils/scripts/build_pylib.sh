
origin="${PWD}"
autorest --namespace=RubrikLib --output-folder=RubrikLib --override-client-name=RubrikLib --python --input-file=../swagger/api-docs-v1-mod
autorest --namespace=RubrikLib_Int --output-folder=RubrikLib_Int --override-client-name=RubrikLib_Int --python --input-file=../swagger/api-docs-internal-mod
cd ../RubrikLib
python setup.py build
cd ../RubrikLib_Int
python setup.py build
cd $origin