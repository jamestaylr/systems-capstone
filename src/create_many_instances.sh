for x in {2..10};
do 

	python create_instance.py -n c$x | grep floating_ip_address > tmp.txt
	IPLINE=`cat tmp.txt`
	rm tmp.txt
	echo $IPLINE

	PART=$(echo "$IPLINE" | tr '[|]' ' ')
	ip=$(echo $PART | cut -d " " -f 2)
	echo $ip	

	COLON=":"
	COMBO=cirros@$ip$COLON
	echo $COMBO

	sleep 30
	echo `scp -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -i ../../devstack/id_rsa_demo ../stress $COMBO`
	echo `scp -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -i ../../devstack/id_rsa_demo run_forever.sh $COMBO`
	echo `nohup ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -i ../../devstack/id_rsa_demo   cirros@$ip './run_forever.sh' > out_$ip.txt &`
done
