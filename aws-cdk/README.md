## Prerequisites
You have to have aws cli, cdk, python3 and virtualenv installed.
```bash
~/k8s-labs$ aws --version
aws-cli/2.15.32 Python/3.11.8 Linux/5.15.146.1-microsoft-standard-WSL2 exe/x86_64.ubuntu.22 prompt/off
~/k8s-labs/aws-cdk$ cdk --version
2.133.0 (build dcc1e75)
~/k8s-labs/aws-cdk$ python3 --version
Python 3.10.12
~/k8s-labs$ sudo apt install python3-pip
~/k8s-labs$ pip --version
pip 22.0.2 from /usr/lib/python3/dist-packages/pip (python 3.10)
~/k8s-labs$ python3 -m pip install --user virtualenv
~/k8s-labs$ python3 -m virtualenv --version
virtualenv 20.25.1 from /home/vma/.local/lib/python3.10/site-packages/virtualenv/__init__.py
```

## To find latest AMI config for this lab
This lab is based on Ubuntu AMI own by [Canonica](https://canonical-aws.readthedocs-hosted.com/en/latest/aws-how-to/instances/find-ubuntu-images/#ownership-verification) account(099720109477). Refer to [Finding images with SSM](https://canonical-aws.readthedocs-hosted.com/en/latest/aws-how-to/instances/find-ubuntu-images/#images-for-ec2-and-eks) to find latest similar AMI name (Referred as IMAGE_ID in config.json)

```bash
aws ssm get-parameters-by-path --recursive \
    --path /aws/service/canonical/ubuntu/server/20.04/stable/current \
    --query "Parameters[].Name"
# Pick one of them. To save cost, using the arm architect with t4g.small type
ID=$(aws ssm get-parameters \
    --names    /aws/service/canonical/ubuntu/server/20.04/stable/current/arm64/hvm/ebs-gp2/ami-id \
    --query "Parameters[].Value" \
    --output text)
aws ec2 describe-images --image-id $ID --query "Images[].Name" --output text
```
You can find the same AMI with AWS EC2 console AMIs page (or aws cli) with filters:
```bash
aws ec2 describe-images \
    --owners 099720109477 \
    --filters "Name=architecture,Values=arm64" \
    --query "Images[?contains(Name, 'ubuntu/images/hvm-ssd/ubuntu-focal-20.04')].Name" \
    --output yaml | sort | tail -1
 ```