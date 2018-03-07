# KafkaOnNodes
用于部署分布式系统的工具，实现如下功能：

* ssh本地转发

在`conf/nodes_forward.json`中，可修改：`remote_nodes`为目标主机信息，包括name，host（有堡垒机则`server_node`可识别ip即可，无堡垒机本地主机可识别即可），ssh端口port

对于有堡垒机的目标主机，需将堡垒机信息写到`conf/nodes_forward.json`的`server_node`中，同时`conf/conf.json`的`machine`改为`local`表明需要ssh本地转发,否则改为其他。`conf/conf.json`中的key和user为本地主机下进行ssh登录目标主机需要的username和private key。

* 各主机执行命令

在`conf/exec_list.json`中，可修改。

* 上下传

将project中的`resource/upload`下的文件、文件夹上传到所有目标主机
将所有目标主机中`~/folder_from_server`下的文件、文件夹都下载到本地

