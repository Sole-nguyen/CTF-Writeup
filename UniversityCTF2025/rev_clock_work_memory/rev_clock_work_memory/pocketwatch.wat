(module
  (type (;0;) (func))
  (type (;1;) (func (param i32) (result i32)))
  (type (;2;) (func (param i32)))
  (type (;3;) (func (result i32)))
  (func (;0;) (type 0)
    nop)
  (func (;1;) (type 1) (param i32) (result i32)
    (local i32 i32 i32 i32)
    global.get 0
    i32.const 32
    i32.sub
    local.tee 2
    global.set 0
    local.get 2
    i32.const 1262702420
    i32.store offset=27 align=1
    loop  ;; label = @1
      local.get 1
      local.get 2
      i32.add
      local.get 2
      i32.const 27
      i32.add
      local.get 1
      i32.const 3
      i32.and
      i32.add
      i32.load8_u
      local.get 1
      i32.load8_u offset=1024
      i32.xor
      i32.store8
      local.get 1
      i32.const 1
      i32.add
      local.tee 1
      i32.const 23
      i32.ne
      br_if 0 (;@1;)
    end
    local.get 2
    i32.const 0
    i32.store8 offset=23
    block  ;; label = @1
      local.get 0
      i32.load8_u
      local.tee 3
      i32.eqz
      local.get 3
      local.get 2
      local.tee 1
      i32.load8_u
      local.tee 4
      i32.ne
      i32.or
      br_if 0 (;@1;)
      loop  ;; label = @2
        local.get 1
        i32.load8_u offset=1
        local.set 4
        local.get 0
        i32.load8_u offset=1
        local.tee 3
        i32.eqz
        br_if 1 (;@1;)
        local.get 1
        i32.const 1
        i32.add
        local.set 1
        local.get 0
        i32.const 1
        i32.add
        local.set 0
        local.get 3
        local.get 4
        i32.eq
        br_if 0 (;@2;)
      end
    end
    local.get 3
    local.get 4
    i32.sub
    local.set 0
    local.get 2
    i32.const 32
    i32.add
    global.set 0
    local.get 0
    i32.eqz)
  (func (;2;) (type 2) (param i32)
    local.get 0
    global.set 0)
  (func (;3;) (type 3) (result i32)
    global.get 0)
  (table (;0;) 2 2 funcref)
  (memory (;0;) 258 258)
  (global (;0;) (mut i32) (i32.const 66592))
  (export "memory" (memory 0))
  (export "check_flag" (func 1))
  (export "__indirect_function_table" (table 0))
  (export "_initialize" (func 0))
  (export "_emscripten_stack_restore" (func 2))
  (export "emscripten_stack_get_current" (func 3))
  (elem (;0;) (i32.const 1) func 0)
  (data (;0;) (i32.const 1024) "\1c\1b\010#{0&\0b=p=\0b~0\147\7fs'un>"))
