function generate_private_key_file_if_not_exist() {
    private_key_path=$1
    if [ ! -f "$private_key_path" ]; then
        echo "private key doesn't exist, create it."
        echo 'y/n' | ssh-keygen -f "$private_key_path" -t rsa -N ''
    fi
}

KEY_DIR=resource/key
PRIVATE_KEY_PATH=$KEY_DIR/id_rsa
TOKEN_PATH=$KEY_DIR/token.txt

mkdir -p $KEY_DIR
echo "check private key existence."
generate_private_key_file_if_not_exist $PRIVATE_KEY_PATH

cdk synth
cdk deploy '*' --require-approval never