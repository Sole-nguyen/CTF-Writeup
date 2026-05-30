
ragebait?token=eyJ1c2VyX2lkIjo1NjAsInRlYW1faWQiOjEzMiwiZmlsZV9pZCI6MjN9.acfhdw.3UOLczi_As8E9ojHiKiZU69FrSY:     file format elf64-x86-64


Disassembly of section .text:

00000000004030e6 <.text+0x1fb6>:
  4030e6:	f3 0f 1e fa          	endbr64 
  4030ea:	55                   	push   rbp
  4030eb:	48 89 e5             	mov    rbp,rsp
  4030ee:	48 83 ec 60          	sub    rsp,0x60
  4030f2:	48 89 7d a8          	mov    QWORD PTR [rbp-0x58],rdi
  4030f6:	64 48 8b 04 25 28 00 	mov    rax,QWORD PTR fs:0x28
  4030fd:	00 00 
  4030ff:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
  403103:	31 c0                	xor    eax,eax
  403105:	c7 45 b4 5b 0a 00 00 	mov    DWORD PTR [rbp-0x4c],0xa5b
  40310c:	8b 45 b4             	mov    eax,DWORD PTR [rbp-0x4c]
  40310f:	83 f0 fe             	xor    eax,0xfffffffe
  403112:	89 c2                	mov    edx,eax
  403114:	8b 45 b4             	mov    eax,DWORD PTR [rbp-0x4c]
  403117:	83 e0 fe             	and    eax,0xfffffffe
  40311a:	01 c0                	add    eax,eax
  40311c:	01 d0                	add    eax,edx
  40311e:	83 c0 01             	add    eax,0x1
  403121:	89 45 b4             	mov    DWORD PTR [rbp-0x4c],eax
  403124:	8b 45 b4             	mov    eax,DWORD PTR [rbp-0x4c]
  403127:	0c ac                	or     al,0xac
  403129:	89 c2                	mov    edx,eax
  40312b:	8b 45 b4             	mov    eax,DWORD PTR [rbp-0x4c]
  40312e:	25 ac 00 00 00       	and    eax,0xac
  403133:	01 d0                	add    eax,edx
  403135:	89 45 b4             	mov    DWORD PTR [rbp-0x4c],eax
  403138:	8b 45 b4             	mov    eax,DWORD PTR [rbp-0x4c]
  40313b:	0c 9f                	or     al,0x9f
  40313d:	89 c1                	mov    ecx,eax
  40313f:	8b 45 b4             	mov    eax,DWORD PTR [rbp-0x4c]
  403142:	25 9f 00 00 00       	and    eax,0x9f
  403147:	89 c2                	mov    edx,eax
  403149:	89 c8                	mov    eax,ecx
  40314b:	29 d0                	sub    eax,edx
  40314d:	89 45 b4             	mov    DWORD PTR [rbp-0x4c],eax
  403150:	8b 45 b4             	mov    eax,DWORD PTR [rbp-0x4c]
  403153:	35 3c ff ff ff       	xor    eax,0xffffff3c
  403158:	89 c2                	mov    edx,eax
  40315a:	8b 45 b4             	mov    eax,DWORD PTR [rbp-0x4c]
  40315d:	24 3c                	and    al,0x3c
  40315f:	01 c0                	add    eax,eax
  403161:	01 d0                	add    eax,edx
  403163:	83 c0 01             	add    eax,0x1
  403166:	89 45 b4             	mov    DWORD PTR [rbp-0x4c],eax
  403169:	48 b8 b2 88 93 cd c1 	movabs rax,0x888995c1cd9388b2
  403170:	95 89 88 
  403173:	48 ba 92 c1 88 92 c1 	movabs rdx,0xb6c180c19288c192
  40317a:	80 c1 b6 
  40317d:	48 89 45 c0          	mov    QWORD PTR [rbp-0x40],rax
  403181:	48 89 55 c8          	mov    QWORD PTR [rbp-0x38],rdx
  403185:	48 b8 b6 84 8f 85 98 	movabs rax,0xcf92c698858f84b6
  40318c:	c6 92 cf 
  40318f:	48 89 45 cf          	mov    QWORD PTR [rbp-0x31],rax
  403193:	c7 45 b8 00 00 00 00 	mov    DWORD PTR [rbp-0x48],0x0
  40319a:	eb 1c                	jmp    4031b8 <stderr@GLIBC_2.2.5-0x4ce68>
  40319c:	8b 45 b8             	mov    eax,DWORD PTR [rbp-0x48]
  40319f:	48 98                	cdqe   
  4031a1:	0f b6 44 05 c0       	movzx  eax,BYTE PTR [rbp+rax*1-0x40]
  4031a6:	83 f0 e1             	xor    eax,0xffffffe1
  4031a9:	89 c2                	mov    edx,eax
  4031ab:	8b 45 b8             	mov    eax,DWORD PTR [rbp-0x48]
  4031ae:	48 98                	cdqe   
  4031b0:	88 54 05 e0          	mov    BYTE PTR [rbp+rax*1-0x20],dl
  4031b4:	83 45 b8 01          	add    DWORD PTR [rbp-0x48],0x1
  4031b8:	83 7d b8 16          	cmp    DWORD PTR [rbp-0x48],0x16
  4031bc:	7e de                	jle    40319c <stderr@GLIBC_2.2.5-0x4ce84>
  4031be:	c6 45 f7 00          	mov    BYTE PTR [rbp-0x9],0x0
  4031c2:	48 8b 45 a8          	mov    rax,QWORD PTR [rbp-0x58]
  4031c6:	0f b6 00             	movzx  eax,BYTE PTR [rax]
  4031c9:	0f be c0             	movsx  eax,al
  4031cc:	83 c0 0a             	add    eax,0xa
  4031cf:	89 45 bc             	mov    DWORD PTR [rbp-0x44],eax
  4031d2:	eb 3c                	jmp    403210 <stderr@GLIBC_2.2.5-0x4ce10>
  4031d4:	8b 45 bc             	mov    eax,DWORD PTR [rbp-0x44]
  4031d7:	83 e0 01             	and    eax,0x1
  4031da:	85 c0                	test   eax,eax
  4031dc:	75 07                	jne    4031e5 <stderr@GLIBC_2.2.5-0x4ce3b>
  4031de:	8b 45 bc             	mov    eax,DWORD PTR [rbp-0x44]
  4031e1:	d1 e8                	shr    eax,1
  4031e3:	eb 21                	jmp    403206 <stderr@GLIBC_2.2.5-0x4ce1a>
  4031e5:	8b 55 bc             	mov    edx,DWORD PTR [rbp-0x44]
  4031e8:	89 d0                	mov    eax,edx
  4031ea:	01 c0                	add    eax,eax
  4031ec:	01 d0                	add    eax,edx
  4031ee:	83 f0 fe             	xor    eax,0xfffffffe
  4031f1:	89 c1                	mov    ecx,eax
  4031f3:	8b 55 bc             	mov    edx,DWORD PTR [rbp-0x44]
  4031f6:	89 d0                	mov    eax,edx
  4031f8:	01 c0                	add    eax,eax
  4031fa:	01 d0                	add    eax,edx
  4031fc:	83 e0 fe             	and    eax,0xfffffffe
  4031ff:	01 c0                	add    eax,eax
  403201:	01 c8                	add    eax,ecx
  403203:	83 c0 01             	add    eax,0x1
  403206:	89 45 bc             	mov    DWORD PTR [rbp-0x44],eax
  403209:	8b 45 b4             	mov    eax,DWORD PTR [rbp-0x4c]
  40320c:	85 c0                	test   eax,eax
  40320e:	74 08                	je     403218 <stderr@GLIBC_2.2.5-0x4ce08>
  403210:	83 7d bc 01          	cmp    DWORD PTR [rbp-0x44],0x1
  403214:	75 be                	jne    4031d4 <stderr@GLIBC_2.2.5-0x4ce4c>
  403216:	eb 01                	jmp    403219 <stderr@GLIBC_2.2.5-0x4ce07>
  403218:	90                   	nop
  403219:	48 8d 45 e0          	lea    rax,[rbp-0x20]
  40321d:	48 89 c7             	mov    rdi,rax
  403220:	e8 8b de ff ff       	call   4010b0 <stderr@GLIBC_2.2.5-0x4ef70>
  403225:	bf 01 00 00 00       	mov    edi,0x1
  40322a:	e8 e1 de ff ff       	call   401110 <stderr@GLIBC_2.2.5-0x4ef10>
  40322f:	f3 0f 1e fa          	endbr64 
  403233:	55                   	push   rbp
  403234:	48 89 e5             	mov    rbp,rsp
  403237:	48 83 ec 60          	sub    rsp,0x60
  40323b:	48 89 7d a8          	mov    QWORD PTR [rbp-0x58],rdi
  40323f:	64 48 8b 04 25 28 00 	mov    rax,QWORD PTR fs:0x28
  403246:	00 00 
  403248:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
  40324c:	31 c0                	xor    eax,eax
  40324e:	c7 45 b8 18 84 00 00 	mov    DWORD PTR [rbp-0x48],0x8418
  403255:	8b 45 b8             	mov    eax,DWORD PTR [rbp-0x48]
  403258:	83 f0 75             	xor    eax,0x75
  40325b:	89 45 b8             	mov    DWORD PTR [rbp-0x48],eax
  40325e:	8b 45 b8             	mov    eax,DWORD PTR [rbp-0x48]
  403261:	83 f0 f1             	xor    eax,0xfffffff1
  403264:	89 c2                	mov    edx,eax
  403266:	8b 45 b8             	mov    eax,DWORD PTR [rbp-0x48]
  403269:	83 e0 f1             	and    eax,0xfffffff1
  40326c:	01 c0                	add    eax,eax
  40326e:	01 d0                	add    eax,edx
  403270:	83 c0 01             	add    eax,0x1
  403273:	89 45 b8             	mov    DWORD PTR [rbp-0x48],eax
  403276:	48 b8 b8 bb a9 b2 e0 	movabs rax,0xa3a9fae0b2a9bbb8
  40327d:	fa a9 a3 
  403280:	48 ba b4 ae bb a2 fa 	movabs rdx,0xa8a8bffaa2bbaeb4
  403287:	bf a8 a8 
  40328a:	48 89 45 c0          	mov    QWORD PTR [rbp-0x40],rax
  40328e:	48 89 55 c8          	mov    QWORD PTR [rbp-0x38],rdx
  403292:	66 c7 45 d0 b5 a8    	mov    WORD PTR [rbp-0x30],0xa8b5
  403298:	c7 45 bc 00 00 00 00 	mov    DWORD PTR [rbp-0x44],0x0
  40329f:	eb 31                	jmp    4032d2 <stderr@GLIBC_2.2.5-0x4cd4e>
  4032a1:	8b 45 bc             	mov    eax,DWORD PTR [rbp-0x44]
  4032a4:	48 98                	cdqe   
  4032a6:	0f b6 44 05 c0       	movzx  eax,BYTE PTR [rbp+rax*1-0x40]
  4032ab:	83 c8 da             	or     eax,0xffffffda
  4032ae:	89 c2                	mov    edx,eax
  4032b0:	8b 45 bc             	mov    eax,DWORD PTR [rbp-0x44]
  4032b3:	48 98                	cdqe   
  4032b5:	0f b6 44 05 c0       	movzx  eax,BYTE PTR [rbp+rax*1-0x40]
  4032ba:	83 e0 da             	and    eax,0xffffffda
  4032bd:	89 c1                	mov    ecx,eax
  4032bf:	89 d0                	mov    eax,edx
  4032c1:	29 c8                	sub    eax,ecx
  4032c3:	89 c2                	mov    edx,eax
  4032c5:	8b 45 bc             	mov    eax,DWORD PTR [rbp-0x44]
  4032c8:	48 98                	cdqe   
  4032ca:	88 54 05 e0          	mov    BYTE PTR [rbp+rax*1-0x20],dl
  4032ce:	83 45 bc 01          	add    DWORD PTR [rbp-0x44],0x1
  4032d2:	83 7d bc 11          	cmp    DWORD PTR [rbp-0x44],0x11
  4032d6:	7e c9                	jle    4032a1 <stderr@GLIBC_2.2.5-0x4cd7f>
  4032d8:	c6 45 f2 00          	mov    BYTE PTR [rbp-0xe],0x0
  4032dc:	48 8b 55 a8          	mov    rdx,QWORD PTR [rbp-0x58]
  4032e0:	48 8d 45 e0          	lea    rax,[rbp-0x20]
  4032e4:	48 89 c6             	mov    rsi,rax
  4032e7:	48 8d 05 59 0d 04 00 	lea    rax,[rip+0x40d59]        # 444047 <stderr@GLIBC_2.2.5-0xbfd9>
  4032ee:	48 89 c7             	mov    rdi,rax
  4032f1:	b8 00 00 00 00       	mov    eax,0x0
  4032f6:	e8 e5 dd ff ff       	call   4010e0 <stderr@GLIBC_2.2.5-0x4ef40>
  4032fb:	bf 7f 00 00 00       	mov    edi,0x7f
  403300:	e8 0b de ff ff       	call   401110 <stderr@GLIBC_2.2.5-0x4ef10>
  403305:	f3                   	repz
