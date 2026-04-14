# 在 copy_generator.py 开头添加
try:
    from scripts.adversarial_generator import AdversarialContentGenerator
except ImportError:
    AdversarialContentGenerator = None

# 修改 __init__ 方法，添加对抗式生成支持
# use_adversarial: bool = False
# adversarial_iterations: int = 3
