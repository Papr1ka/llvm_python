from llvm_python import parse_assembly
from llvm_python.utils import dump


ir_text = """; Function Attrs: noinline nounwind optnone uwtable
define dso_local i32 @factorial_req(i32 noundef %0) #0 {
  %2 = alloca i32, align 4
  %3 = alloca i32, align 4
  store i32 %0, ptr %3, align 4
  %4 = load i32, ptr %3, align 4
  %5 = icmp eq i32 %4, 1
  br i1 %5, label %6, label %7

6:                                                ; preds = %1
  store i32 1, ptr %2, align 4
  br label %13

7:                                                ; preds = %1
  %8 = load i32, ptr %3, align 4
  %9 = sub nsw i32 %8, 1
  %10 = call i32 @factorial_req(i32 noundef %9)
  %11 = load i32, ptr %3, align 4
  %12 = mul nsw i32 %10, %11
  store i32 %12, ptr %2, align 4
  br label %13

13:                                               ; preds = %7, %6
  %14 = load i32, ptr %2, align 4
  ret i32 %14
}"""

dumped_ir = """Function([Argument(0, '%0', Type('i32', <TypeID.IntegerTyID: 13>))], [[], [], ['noundef']], [Block([Instruction(31, 'alloca', [Value('1', Type('i32', <TypeID.IntegerTyID: 13>))], '%2', Type('ptr', <TypeID.PointerTyID: 15>)), Instruction(31, 'alloca', [Value('1', Type('i32', <TypeID.IntegerTyID: 13>))], '%3', Type('ptr', <TypeID.PointerTyID: 15>)), Instruction(33, 'store', [Value('%0', Type('i32', <TypeID.IntegerTyID: 13>)), Value('%3', Type('ptr', <TypeID.PointerTyID: 15>))], '<badref>', Type('void', <TypeID.VoidTyID: 7>)), Instruction(32, 'load', [Value('%3', Type('ptr', <TypeID.PointerTyID: 15>))], '%4', Type('i32', <TypeID.IntegerTyID: 13>)), Instruction(53, 'icmp', [Value('%4', Type('i32', <TypeID.IntegerTyID: 13>)), Value('1', Type('i32', <TypeID.IntegerTyID: 13>))], '%5', Type('i1', <TypeID.IntegerTyID: 13>)), Instruction(2, 'br', [Value('%5', Type('i1', <TypeID.IntegerTyID: 13>)), Value('%7', Type('label', <TypeID.LabelTyID: 8>)), Value('%6', Type('label', <TypeID.LabelTyID: 8>))], '<badref>', Type('void', <TypeID.VoidTyID: 7>))], '%1', [], Type('label', <TypeID.LabelTyID: 8>)), Block([Instruction(33, 'store', [Value('1', Type('i32', <TypeID.IntegerTyID: 13>)), Value('%2', Type('ptr', <TypeID.PointerTyID: 15>))], '<badref>', Type('void', <TypeID.VoidTyID: 7>)), Instruction(2, 'br', [Value('%13', Type('label', <TypeID.LabelTyID: 8>))], '<badref>', Type('void', <TypeID.VoidTyID: 7>))], '%6', ['%1'], Type('label', <TypeID.LabelTyID: 8>)), Block([Instruction(32, 'load', [Value('%3', Type('ptr', <TypeID.PointerTyID: 15>))], '%8', Type('i32', <TypeID.IntegerTyID: 13>)), Instruction(15, 'sub', [Value('%8', Type('i32', <TypeID.IntegerTyID: 13>)), Value('1', Type('i32', <TypeID.IntegerTyID: 13>))], '%9', Type('i32', <TypeID.IntegerTyID: 13>)), Instruction(56, 'call', [Value('%9', Type('i32', <TypeID.IntegerTyID: 13>)), Value('factorial_req', Type('ptr', <TypeID.PointerTyID: 15>))], '%10', Type('i32', <TypeID.IntegerTyID: 13>)), Instruction(32, 'load', [Value('%3', Type('ptr', <TypeID.PointerTyID: 15>))], '%11', Type('i32', <TypeID.IntegerTyID: 13>)), Instruction(17, 'mul', [Value('%10', Type('i32', <TypeID.IntegerTyID: 13>)), Value('%11', Type('i32', <TypeID.IntegerTyID: 13>))], '%12', Type('i32', <TypeID.IntegerTyID: 13>)), Instruction(33, 'store', [Value('%12', Type('i32', <TypeID.IntegerTyID: 13>)), Value('%2', Type('ptr', <TypeID.PointerTyID: 15>))], '<badref>', Type('void', <TypeID.VoidTyID: 7>)), Instruction(2, 'br', [Value('%13', Type('label', <TypeID.LabelTyID: 8>))], '<badref>', Type('void', <TypeID.VoidTyID: 7>))], '%7', ['%1'], Type('label', <TypeID.LabelTyID: 8>)), Block([Instruction(32, 'load', [Value('%2', Type('ptr', <TypeID.PointerTyID: 15>))], '%14', Type('i32', <TypeID.IntegerTyID: 13>)), Instruction(1, 'ret', [Value('%14', Type('i32', <TypeID.IntegerTyID: 13>))], '<badref>', Type('void', <TypeID.VoidTyID: 7>))], '%13', ['%7', '%6'], Type('label', <TypeID.LabelTyID: 8>))], 0, 0, 0, Type('i32', <TypeID.IntegerTyID: 13>), 'factorial_req', Type('ptr', <TypeID.PointerTyID: 15>))"""

module = parse_assembly(ir_text)
function = module.get_function("factorial_req")
dumped = dump(function, annotate_fields=False)
assert dumped_ir == dumped, "Dump is different from the original:\n" + dumped_ir