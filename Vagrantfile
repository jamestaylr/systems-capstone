# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure(2) do |config|
  for i in 1..3 do
    config.vm.define "vm#{i}" do |vm1|
      vm1.vm.box = "ktr/mininet"
      vm1.vm.network "public_network"
      vm1.vm.network :forwarded_port, guest: 22, host: rand(2000...4000), id: 'ssh'
  
      vm1.ssh.forward_x11 = true
      vm1.ssh.forward_agent = true
      vm1.vm.provider "virtualbox" do |vb|
        vb.customize ["modifyvm", :id, "--vram", "128"]
        vb.memory = "2404"
        vb.cpus = "2"
      end
    end
  end
end
