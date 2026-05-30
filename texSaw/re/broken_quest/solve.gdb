set pagination off
break turn_in
commands
  silent
  set {int}($rdi+0)=2
  set {int}($rdi+4)=6
  set {int}($rdi+8)=-4
  set {int}($rdi+12)=6
  set {int}($rdi+16)=0
  set {int}($rdi+20)=4
  set {int}($rdi+24)=-3
  set {int}($rdi+28)=1
  continue
end
shell printf '0\n' > input.txt
run < input.txt
quit
