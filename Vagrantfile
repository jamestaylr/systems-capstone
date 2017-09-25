# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure(2) do |config|
  config.vm.box = "bingmann/ubuntu-8.04.4-i386"
  config.vm.network "public_network"
  config.vm.network :forwarded_port, guest: 22, host: rand(2000...4000), id: 'ssh'

  config.vm.provider "virtualbox" do |vb|
    vb.customize ["modifyvm", :id, "--vram", "128"]
    vb.memory = "2404"
    vb.cpus = "2"
  end

  config.vm.provision "shell", path: "provision.sh"
end
