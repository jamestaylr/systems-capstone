live migration notes and observations 

---

if you get `Policy doesn't allow os_compute_api:os-services to be performed.` error --> make sure you are running openstack cli as admin

if you create an instance and has an error status, and the gui says `No sql_connection parameter is established
Code` --> run `nova-manage db sync`
