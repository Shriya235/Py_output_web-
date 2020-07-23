import config1 as conf
import commonfunc1 as cf

cf.Data_preparation(conf.logfile,conf.avg,conf.memory)
cf.uptime(conf.logfile)
cf.network(conf.nwfile)
cf.picrep(conf.topo)
