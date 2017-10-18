directory '/etc/chef' do
  owner 'root'
  group 'root'
  mode '0755'
  action :nothing
end.run_action(:create)

cookbook_file '/etc/chef/openstack_data_bag_secret' do
  #source "#{File.dirname(__FILE__)}/../../../../../encrypted_data_bag_secret"
  source 'encrypted_data_bag_secret'
  owner 'root'
  group 'root'
  mode '0755'
  action :nothing
end.run_action(:create)

bash 'increase_swap' do
  code <<-EOH
    grep -q 'swapfile' /etc/fstab
    if [ $? -ne 0 ]; then
        fallocate -l 6000M /swapfile
        chmod 600 /swapfile
        mkswap /swapfile
        swapon /swapfile
        echo '/swapfile none swap defaults 0 0' >> /etc/fstab
    fi
    EOH
  action :nothing
end.run_action(:run)
