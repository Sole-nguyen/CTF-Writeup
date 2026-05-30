
ragebait?token=eyJ1c2VyX2lkIjo1NjAsInRlYW1faWQiOjEzMiwiZmlsZV9pZCI6MjN9.acfhdw.3UOLczi_As8E9ojHiKiZU69FrSY:     file format elf64-x86-64


Disassembly of section .text:

0000000000418644 <.text+0x17514>:
  418644:	f3 0f 1e fa          	endbr64 
  418648:	55                   	push   rbp
  418649:	48 89 e5             	mov    rbp,rsp
  41864c:	48 83 ec 70          	sub    rsp,0x70
  418650:	48 89 7d 98          	mov    QWORD PTR [rbp-0x68],rdi
  418654:	64 48 8b 04 25 28 00 	mov    rax,QWORD PTR fs:0x28
  41865b:	00 00 
  41865d:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
  418661:	31 c0                	xor    eax,eax
  418663:	c7 45 a4 60 f3 00 00 	mov    DWORD PTR [rbp-0x5c],0xf360
  41866a:	8b 45 a4             	mov    eax,DWORD PTR [rbp-0x5c]
  41866d:	35 26 ff ff ff       	xor    eax,0xffffff26
  418672:	89 c2                	mov    edx,eax
  418674:	8b 45 a4             	mov    eax,DWORD PTR [rbp-0x5c]
  418677:	24 26                	and    al,0x26
  418679:	01 c0                	add    eax,eax
  41867b:	01 d0                	add    eax,edx
  41867d:	83 c0 01             	add    eax,0x1
  418680:	89 45 a4             	mov    DWORD PTR [rbp-0x5c],eax
  418683:	8b 45 a4             	mov    eax,DWORD PTR [rbp-0x5c]
  418686:	34 9f                	xor    al,0x9f
  418688:	89 45 a4             	mov    DWORD PTR [rbp-0x5c],eax
  41868b:	8b 45 a4             	mov    eax,DWORD PTR [rbp-0x5c]
  41868e:	83 f0 31             	xor    eax,0x31
  418691:	89 c2                	mov    edx,eax
  418693:	8b 45 a4             	mov    eax,DWORD PTR [rbp-0x5c]
  418696:	83 e0 31             	and    eax,0x31
  418699:	01 c0                	add    eax,eax
  41869b:	01 d0                	add    eax,edx
  41869d:	89 45 a4             	mov    DWORD PTR [rbp-0x5c],eax
  4186a0:	8b 45 a4             	mov    eax,DWORD PTR [rbp-0x5c]
  4186a3:	83 f0 e4             	xor    eax,0xffffffe4
  4186a6:	89 c2                	mov    edx,eax
  4186a8:	8b 45 a4             	mov    eax,DWORD PTR [rbp-0x5c]
  4186ab:	83 e0 e4             	and    eax,0xffffffe4
  4186ae:	01 c0                	add    eax,eax
  4186b0:	01 d0                	add    eax,edx
  4186b2:	83 c0 01             	add    eax,0x1
  4186b5:	89 45 a4             	mov    DWORD PTR [rbp-0x5c],eax
  4186b8:	48 b8 e8 df df c2 df 	movabs rax,0x9c998ddfc2dfdfe8
  4186bf:	8d 99 9c 
  4186c2:	48 ba 95 97 8d e4 8a 	movabs rdx,0xcc8dc08ae48d9795
  4186c9:	c0 8d cc 
  4186cc:	48 89 45 b0          	mov    QWORD PTR [rbp-0x50],rax
  4186d0:	48 89 55 b8          	mov    QWORD PTR [rbp-0x48],rdx
  4186d4:	48 b8 8d d9 c8 cc dd 	movabs rax,0x83d9c2ddccc8d98d
  4186db:	c2 d9 83 
  4186de:	48 89 45 c0          	mov    QWORD PTR [rbp-0x40],rax
  4186e2:	c7 45 a8 00 00 00 00 	mov    DWORD PTR [rbp-0x58],0x0
  4186e9:	eb 31                	jmp    41871c <stderr@GLIBC_2.2.5-0x37904>
  4186eb:	8b 45 a8             	mov    eax,DWORD PTR [rbp-0x58]
  4186ee:	48 98                	cdqe   
  4186f0:	0f b6 44 05 b0       	movzx  eax,BYTE PTR [rbp+rax*1-0x50]
  4186f5:	83 c8 ad             	or     eax,0xffffffad
  4186f8:	89 c2                	mov    edx,eax
  4186fa:	8b 45 a8             	mov    eax,DWORD PTR [rbp-0x58]
  4186fd:	48 98                	cdqe   
  4186ff:	0f b6 44 05 b0       	movzx  eax,BYTE PTR [rbp+rax*1-0x50]
  418704:	83 e0 ad             	and    eax,0xffffffad
  418707:	89 c1                	mov    ecx,eax
  418709:	89 d0                	mov    eax,edx
  41870b:	29 c8                	sub    eax,ecx
  41870d:	89 c2                	mov    edx,eax
  41870f:	8b 45 a8             	mov    eax,DWORD PTR [rbp-0x58]
  418712:	48 98                	cdqe   
  418714:	88 54 05 d0          	mov    BYTE PTR [rbp+rax*1-0x30],dl
  418718:	83 45 a8 01          	add    DWORD PTR [rbp-0x58],0x1
  41871c:	83 7d a8 17          	cmp    DWORD PTR [rbp-0x58],0x17
  418720:	7e c9                	jle    4186eb <stderr@GLIBC_2.2.5-0x37935>
  418722:	c6 45 e8 00          	mov    BYTE PTR [rbp-0x18],0x0
  418726:	48 8b 45 98          	mov    rax,QWORD PTR [rbp-0x68]
  41872a:	0f b6 00             	movzx  eax,BYTE PTR [rax]
  41872d:	0f be c0             	movsx  eax,al
  418730:	83 c0 01             	add    eax,0x1
  418733:	89 45 ac             	mov    DWORD PTR [rbp-0x54],eax
  418736:	eb 3c                	jmp    418774 <stderr@GLIBC_2.2.5-0x378ac>
  418738:	8b 45 ac             	mov    eax,DWORD PTR [rbp-0x54]
  41873b:	83 e0 01             	and    eax,0x1
  41873e:	85 c0                	test   eax,eax
  418740:	75 07                	jne    418749 <stderr@GLIBC_2.2.5-0x378d7>
  418742:	8b 45 ac             	mov    eax,DWORD PTR [rbp-0x54]
  418745:	d1 e8                	shr    eax,1
  418747:	eb 21                	jmp    41876a <stderr@GLIBC_2.2.5-0x378b6>
  418749:	8b 55 ac             	mov    edx,DWORD PTR [rbp-0x54]
  41874c:	89 d0                	mov    eax,edx
  41874e:	01 c0                	add    eax,eax
  418750:	01 d0                	add    eax,edx
  418752:	83 f0 fe             	xor    eax,0xfffffffe
  418755:	89 c1                	mov    ecx,eax
  418757:	8b 55 ac             	mov    edx,DWORD PTR [rbp-0x54]
  41875a:	89 d0                	mov    eax,edx
  41875c:	01 c0                	add    eax,eax
  41875e:	01 d0                	add    eax,edx
  418760:	83 e0 fe             	and    eax,0xfffffffe
  418763:	01 c0                	add    eax,eax
  418765:	01 c8                	add    eax,ecx
  418767:	83 c0 01             	add    eax,0x1
  41876a:	89 45 ac             	mov    DWORD PTR [rbp-0x54],eax
  41876d:	8b 45 a4             	mov    eax,DWORD PTR [rbp-0x5c]
  418770:	85 c0                	test   eax,eax
  418772:	74 08                	je     41877c <stderr@GLIBC_2.2.5-0x378a4>
  418774:	83 7d ac 01          	cmp    DWORD PTR [rbp-0x54],0x1
  418778:	75 be                	jne    418738 <stderr@GLIBC_2.2.5-0x378e8>
  41877a:	eb 01                	jmp    41877d <stderr@GLIBC_2.2.5-0x378a3>
  41877c:	90                   	nop
  41877d:	48 8d 45 d0          	lea    rax,[rbp-0x30]
  418781:	48 89 c7             	mov    rdi,rax
  418784:	e8 27 89 fe ff       	call   4010b0 <stderr@GLIBC_2.2.5-0x4ef70>
  418789:	bf 01 00 00 00       	mov    edi,0x1
  41878e:	e8 7d 89 fe ff       	call   401110 <stderr@GLIBC_2.2.5-0x4ef10>
  418793:	f3 0f 1e fa          	endbr64 
  418797:	55                   	push   rbp
  418798:	48 89 e5             	mov    rbp,rsp
  41879b:	48 83 ec 70          	sub    rsp,0x70
  41879f:	48 89 7d 98          	mov    QWORD PTR [rbp-0x68],rdi
  4187a3:	64 48 8b 04 25 28 00 	mov    rax,QWORD PTR fs:0x28
  4187aa:	00 00 
  4187ac:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
  4187b0:	31 c0                	xor    eax,eax
  4187b2:	c7 45 a4 3d 8e 00 00 	mov    DWORD PTR [rbp-0x5c],0x8e3d
  4187b9:	8b 45 a4             	mov    eax,DWORD PTR [rbp-0x5c]
  4187bc:	83 f0 74             	xor    eax,0x74
  4187bf:	89 45 a4             	mov    DWORD PTR [rbp-0x5c],eax
  4187c2:	8b 45 a4             	mov    eax,DWORD PTR [rbp-0x5c]
  4187c5:	83 f0 a5             	xor    eax,0xffffffa5
  4187c8:	89 c2                	mov    edx,eax
  4187ca:	8b 45 a4             	mov    eax,DWORD PTR [rbp-0x5c]
  4187cd:	83 e0 a5             	and    eax,0xffffffa5
  4187d0:	01 c0                	add    eax,eax
  4187d2:	01 d0                	add    eax,edx
  4187d4:	83 c0 01             	add    eax,0x1
  4187d7:	89 45 a4             	mov    DWORD PTR [rbp-0x5c],eax
  4187da:	48 b8 82 b7 a5 bd f6 	movabs rax,0xbfb7b0f6bda5b782
  4187e1:	b0 b7 bf 
  4187e4:	48 ba ba b3 b2 f6 a5 	movabs rdx,0xb5b5a3a5f6b2b3ba
  4187eb:	a3 b5 b5 
  4187ee:	48 89 45 b0          	mov    QWORD PTR [rbp-0x50],rax
  4187f2:	48 89 55 b8          	mov    QWORD PTR [rbp-0x48],rdx
  4187f6:	48 b8 b3 b2 f6 a5 a3 	movabs rax,0xb3b5b5a3a5f6b2b3
  4187fd:	b5 b5 b3 
  418800:	48 ba a5 a5 b0 a3 ba 	movabs rdx,0xf8afbabaa3b0a5a5
  418807:	ba af f8 
  41880a:	48 89 45 b9          	mov    QWORD PTR [rbp-0x47],rax
  41880e:	48 89 55 c1          	mov    QWORD PTR [rbp-0x3f],rdx
  418812:	c7 45 a8 00 00 00 00 	mov    DWORD PTR [rbp-0x58],0x0
  418819:	eb 31                	jmp    41884c <stderr@GLIBC_2.2.5-0x377d4>
  41881b:	8b 45 a8             	mov    eax,DWORD PTR [rbp-0x58]
  41881e:	48 98                	cdqe   
  418820:	0f b6 44 05 b0       	movzx  eax,BYTE PTR [rbp+rax*1-0x50]
  418825:	83 c8 d6             	or     eax,0xffffffd6
  418828:	89 c2                	mov    edx,eax
  41882a:	8b 45 a8             	mov    eax,DWORD PTR [rbp-0x58]
  41882d:	48 98                	cdqe   
  41882f:	0f b6 44 05 b0       	movzx  eax,BYTE PTR [rbp+rax*1-0x50]
  418834:	83 e0 d6             	and    eax,0xffffffd6
  418837:	89 c1                	mov    ecx,eax
  418839:	89 d0                	mov    eax,edx
  41883b:	29 c8                	sub    eax,ecx
  41883d:	89 c2                	mov    edx,eax
  41883f:	8b 45 a8             	mov    eax,DWORD PTR [rbp-0x58]
  418842:	48 98                	cdqe   
  418844:	88 54 05 d0          	mov    BYTE PTR [rbp+rax*1-0x30],dl
  418848:	83 45 a8 01          	add    DWORD PTR [rbp-0x58],0x1
  41884c:	83 7d a8 18          	cmp    DWORD PTR [rbp-0x58],0x18
  418850:	7e c9                	jle    41881b <stderr@GLIBC_2.2.5-0x37805>
  418852:	c6 45 e9 00          	mov    BYTE PTR [rbp-0x17],0x0
  418856:	48 8b 45 98          	mov    rax,QWORD PTR [rbp-0x68]
  41885a:	0f b6 00             	movzx  eax,BYTE PTR [rax]
  41885d:	0f be c0             	movsx  eax,al
  418860:	83 c0 01             	add    eax,0x1
  418863:	89 45 ac             	mov    DWORD PTR [rbp-0x54],eax
  418866:	eb 27                	jmp    41888f <stderr@GLIBC_2.2.5-0x37791>
  418868:	8b 45 ac             	mov    eax,DWORD PTR [rbp-0x54]
  41886b:	83 e0 01             	and    eax,0x1
  41886e:	85 c0                	test   eax,eax
  418870:	75 07                	jne    418879 <stderr@GLIBC_2.2.5-0x377a7>
  418872:	8b 45 ac             	mov    eax,DWORD PTR [rbp-0x54]
  418875:	d1 e8                	shr    eax,1
  418877:	eb 0c                	jmp    418885 <stderr@GLIBC_2.2.5-0x3779b>
  418879:	8b 55 ac             	mov    edx,DWORD PTR [rbp-0x54]
  41887c:	89 d0                	mov    eax,edx
  41887e:	01 c0                	add    eax,eax
  418880:	01 d0                	add    eax,edx
  418882:	83 c0 01             	add    eax,0x1
  418885:	89 45 ac             	mov    DWORD PTR [rbp-0x54],eax
  418888:	8b 45 a4             	mov    eax,DWORD PTR [rbp-0x5c]
  41888b:	85 c0                	test   eax,eax
  41888d:	74 08                	je     418897 <stderr@GLIBC_2.2.5-0x37789>
  41888f:	83 7d ac 01          	cmp    DWORD PTR [rbp-0x54],0x1
  418893:	75 d3                	jne    418868 <stderr@GLIBC_2.2.5-0x377b8>
  418895:	eb 01                	jmp    418898 <stderr@GLIBC_2.2.5-0x37788>
  418897:	90                   	nop
  418898:	48 8d 45 d0          	lea    rax,[rbp-0x30]
  41889c:	48 89 c7             	mov    rdi,rax
  41889f:	e8 0c 88 fe ff       	call   4010b0 <stderr@GLIBC_2.2.5-0x4ef70>
  4188a4:	bf 01 00 00 00       	mov    edi,0x1
  4188a9:	e8 62 88 fe ff       	call   401110 <stderr@GLIBC_2.2.5-0x4ef10>
  4188ae:	f3 0f 1e fa          	endbr64 
  4188b2:	55                   	push   rbp
  4188b3:	48 89 e5             	mov    rbp,rsp
  4188b6:	48 83 ec 60          	sub    rsp,0x60
  4188ba:	48 89 7d a8          	mov    QWORD PTR [rbp-0x58],rdi
  4188be:	64 48 8b 04 25 28 00 	mov    rax,QWORD PTR fs:0x28
  4188c5:	00 00 
  4188c7:	48 89 45 f8          	mov    QWORD PTR [rbp-0x8],rax
  4188cb:	31 c0                	xor    eax,eax
  4188cd:	c7 45 b8 01 4d 00 00 	mov    DWORD PTR [rbp-0x48],0x4d01
  4188d4:	8b 45 b8             	mov    eax,DWORD PTR [rbp-0x48]
  4188d7:	34 f4                	xor    al,0xf4
  4188d9:	89 45 b8             	mov    DWORD PTR [rbp-0x48],eax
  4188dc:	8b 55 b8             	mov    edx,DWORD PTR [rbp-0x48]
  4188df:	8b 45 b8             	mov    eax,DWORD PTR [rbp-0x48]
  4188e2:	83 e0 57             	and    eax,0x57
  4188e5:	01 c0                	add    eax,eax
  4188e7:	29 c2                	sub    edx,eax
  4188e9:	8d 42 57             	lea    eax,[rdx+0x57]
  4188ec:	89 45 b8             	mov    DWORD PTR [rbp-0x48],eax
  4188ef:	8b                   	.byte 0x8b
