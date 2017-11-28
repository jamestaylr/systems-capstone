# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure(2) do |config|
  (1..3).each do |i|
    config.vm.define "vm#{i}" do |c|
      c.vm.box = "ubuntu/xenial64"
      c.vm.network "public_network", ip: "169.254.1.#{i}"
      c.vm.network "public_network", :bridge => "eth0"
      c.vm.network :forwarded_port, guest: 22, host: rand(2000...4000), id: 'ssh'
  
      c.ssh.forward_x11 = true
      c.ssh.forward_agent = true
      c.vm.provider "virtualbox" do |vb|
        vb.customize ["modifyvm", :id, "--vram", "128"]
        vb.memory = "2404"
        vb.cpus = "2"
	vb.customize ["modifyvm", :id, "--nicpromisc3", "allow-all"]
      end
    end
  end
end
