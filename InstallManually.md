# For both master and worker
Get 2 Ubuntu boxes with at least 2 CPUs (or kubeadm init will error out). Virtuallization is OK, but don't use Vagrant here because it will by default add another NIC which make things complicated.
```bash
ssh vma@192.168.0.110 # master
ssh vma@192.168.0.111 # worker1
sudo su - 
```

## Install and configure conainerd on masters and workers
```bash 
# Load 2 modules for containerd 运行时所需的内核模块
## Check and create a configuration file to load them after reboot
FILE=/etc/modules-load.d/containerd.conf
ls -l $FILE
cat <<EOF | sudo tee $FILE
overlay
br_netfilter
EOF
cat $FILE
## load them right now before reboot
sudo modprobe overlay
sudo modprobe br_netfilter


# 设置用于配置 Kubernetes CRI 使用的网络参数
FILE=/etc/sysctl.d/99-kubernetes-cri.conf
cat <<EOF | sudo tee $FILE
net.bridge.bridge-nf-call-iptables = 1
net.ipv4.ip_forward = 1
net.bridge.bridge-nf-call-ip6tables = 1
EOF
## and apply those 网络参数
sudo sysctl --system

# Install containerd
sudo apt-get update && sudo apt-get install -y containerd

# generate default config file for containerd
sudo mkdir -p /etc/containerd
sudo containerd config default | sudo tee /etc/containerd/config.toml

# restart containerd and verify it
sudo systemctl restart containerd
sudo systemctl status containerd
```

## Disalbe swap
```bash
# after reboot
    # this sed commands don't work in case the fields are separated by tabs (not spaces). It is better written as 
    # sudo sed -i '/ swap / s/^\(.*\)$/#\1/g' /etc/fstab
    # PS: I also added #? to prevent additional changes to /etc/fstab when the line is already disabled
sudo sed -ri '/\sswap\s/s/^#?/#/' /etc/fstab 

# disable it right now before reboot
sudo swapoff -a
# Verify by making sure Swap is 0 total 0 used 0 free
free 
```

## Install dependencies and all the packages
```bash
# Install the dependencies to downlaod packages
sudo apt-get update && sudo apt-get install -y apt-transport-https curl

# Add the gpg key to the repo - outdated and no long works
# curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -
curl -fsSL https://pkgs.k8s.io/core:/stable:/v1.28/deb/Release.key | sudo gpg --dearmor -o /etc/apt/keyrings/kubernetes-apt-keyring.gpg

# Add kubernetes to the repositories list and update apt - outdated and no longer works
# sudo bash -c 'cat <<EOF >/etc/apt/sources.list.d/kubernetes.list
# deb https://apt.kubernetes.io/ kubernetes-xenial main
# EOF'
echo "deb [signed-by=/etc/apt/keyrings/kubernetes-apt-keyring.gpg] https://pkgs.k8s.io/core:/stable:/v1.28/deb/ /" | sudo tee /etc/apt/sources.list.d/kubernetes.list
sudo apt-get update

# Install all the packages
K8sVersion=1.28.0-1.1
sudo apt-get install -y kubelet=$K8sVersion kubeadm=$K8sVersion kubectl=$K8sVersion --allow-change-held-packages
# Hold, cause we're going to service these packages outside of the normal security updates for the system so that we can control when we move between versions of Kubernetes
sudo apt-mark hold kubelet kubeadm kubectl
```

# For only master

## Create the cluster and verify

```bash
# Create teh cluster - taking some time
sudo kubeadm init --pod-network-cidr 192.168.0.0/16 --kubernetes-version 1.28.0

#Configure our account on the master to have admin access to the API server from a non-privileged account.
mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config
```