"""
Create an arbitrary number of nodes.
Change the for loop as you see fit.

It will start the benchmarking on several nodes.
An output file will be created that you can tail -f 
to see the constantly running benchmarks.


This file assumes the existence of a stresstestapp
benchmarking executable named stress. 
"""
for x in {1..1};
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

	sleep 10
	echo `scp -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -i id_rsa_demo ../stress $COMBO`
	echo `scp -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -i id_rsa_demo run_forever.sh $COMBO`
	echo `nohup ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -i id_rsa_demo   cirros@$ip './run_forever.sh' > out_$ip.txt &`
done
