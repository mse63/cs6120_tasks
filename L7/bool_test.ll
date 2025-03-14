; ModuleID = 'bool_test.c'
source_filename = "bool_test.c"
target datalayout = "e-m:e-p270:32:32-p271:32:32-p272:64:64-i64:64-i128:128-f80:128-n8:16:32:64-S128"
target triple = "x86_64-unknown-linux-gnu"

%struct.__va_list_tag = type { i32, i32, ptr, ptr }

@.str = private unnamed_addr constant [18 x i8] c"Original values:\0A\00", align 1
@.str.1 = private unnamed_addr constant [15 x i8] c"a (true) = %d\0A\00", align 1
@.str.2 = private unnamed_addr constant [16 x i8] c"b (false) = %d\0A\00", align 1
@.str.3 = private unnamed_addr constant [22 x i8] c"\0ALogical operations:\0A\00", align 1
@.str.4 = private unnamed_addr constant [9 x i8] c"!a = %d\0A\00", align 1
@.str.5 = private unnamed_addr constant [13 x i8] c"a && b = %d\0A\00", align 1
@.str.6 = private unnamed_addr constant [13 x i8] c"a || b = %d\0A\00", align 1

; Function Attrs: nounwind sspstrong uwtable
define noundef i32 @main() local_unnamed_addr #0 {
  tail call void (ptr, i64, ...) @_ZL6printfPKcU17pass_object_size1z(ptr noundef nonnull @.str, i64 poison)
  tail call void (ptr, i64, ...) @_ZL6printfPKcU17pass_object_size1z(ptr noundef nonnull @.str.1, i64 poison, i32 noundef 1)
  tail call void (ptr, i64, ...) @_ZL6printfPKcU17pass_object_size1z(ptr noundef nonnull @.str.2, i64 poison, i32 noundef 0)
  tail call void (ptr, i64, ...) @_ZL6printfPKcU17pass_object_size1z(ptr noundef nonnull @.str.3, i64 poison)
  tail call void (ptr, i64, ...) @_ZL6printfPKcU17pass_object_size1z(ptr noundef nonnull @.str.4, i64 poison, i32 noundef 0)
  tail call void (ptr, i64, ...) @_ZL6printfPKcU17pass_object_size1z(ptr noundef nonnull @.str.5, i64 poison, i32 noundef 0)
  tail call void (ptr, i64, ...) @_ZL6printfPKcU17pass_object_size1z(ptr noundef nonnull @.str.6, i64 poison, i32 noundef 1)
  ret i32 0
}

; Function Attrs: mustprogress nocallback nofree nosync nounwind willreturn memory(argmem: readwrite)
declare void @llvm.lifetime.start.p0(i64 immarg, ptr nocapture) #1

; Function Attrs: nounwind sspstrong uwtable
define internal void @_ZL6printfPKcU17pass_object_size1z(ptr noalias noundef %0, i64 %1, ...) unnamed_addr #2 {
  %3 = alloca [1 x %struct.__va_list_tag], align 16
  call void @llvm.lifetime.start.p0(i64 24, ptr nonnull %3) #5
  call void @llvm.va_start.p0(ptr nonnull %3)
  %4 = call i32 @__vprintf_chk(i32 noundef 1, ptr noundef %0, ptr noundef nonnull %3) #5
  call void @llvm.va_end.p0(ptr nonnull %3)
  call void @llvm.lifetime.end.p0(i64 24, ptr nonnull %3) #5
  ret void
}

; Function Attrs: mustprogress nocallback nofree nosync nounwind willreturn memory(argmem: readwrite)
declare void @llvm.lifetime.end.p0(i64 immarg, ptr nocapture) #1

; Function Attrs: mustprogress nocallback nofree nosync nounwind willreturn
declare void @llvm.va_start.p0(ptr) #3

declare i32 @__vprintf_chk(i32 noundef, ptr noundef, ptr noundef) local_unnamed_addr #4

; Function Attrs: mustprogress nocallback nofree nosync nounwind willreturn
declare void @llvm.va_end.p0(ptr) #3

attributes #0 = { nounwind sspstrong uwtable "min-legal-vector-width"="0" "no-trapping-math"="true" "probe-stack"="inline-asm" "stack-protector-buffer-size"="4" "target-cpu"="x86-64" "target-features"="+cmov,+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }
attributes #1 = { mustprogress nocallback nofree nosync nounwind willreturn memory(argmem: readwrite) }
attributes #2 = { nounwind sspstrong uwtable "min-legal-vector-width"="0" "no-trapping-math"="true" "probe-stack"="inline-asm" "stack-protector-buffer-size"="4" "target-cpu"="x86-64" "target-features"="+cmov,+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" "zero-call-used-regs"="used-gpr" }
attributes #3 = { mustprogress nocallback nofree nosync nounwind willreturn }
attributes #4 = { "no-trapping-math"="true" "stack-protector-buffer-size"="4" "target-cpu"="x86-64" "target-features"="+cmov,+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" "zero-call-used-regs"="used-gpr" }
attributes #5 = { nounwind }

!llvm.module.flags = !{!0, !1, !2, !3}
!llvm.ident = !{!4}

!0 = !{i32 1, !"wchar_size", i32 4}
!1 = !{i32 4, !"probe-stack", !"inline-asm"}
!2 = !{i32 8, !"PIC Level", i32 2}
!3 = !{i32 7, !"uwtable", i32 2}
!4 = !{!"clang version 19.1.7"}
