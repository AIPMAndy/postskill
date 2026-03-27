"""
图片生成模块测试
使用 Mock 测试，无需真实 API Key
"""

import pytest
import os
import tempfile
from pathlib import Path

# Mock PonyFlash 类
class MockPonyFlash:
    """Mock PonyFlash 客户端"""
    
    class MockImageResult:
        def __init__(self):
            self.url = "https://example.com/mock-image.png"
    
    class MockImages:
        def generate(self, **kwargs):
            return MockPonyFlash.MockImageResult()
    
    def __init__(self, api_key=None):
        if not api_key:
            raise ValueError("api_key required")
        self.images = self.MockImages()


@pytest.fixture
def mock_ponyflash(monkeypatch):
    """Mock PonyFlash 模块"""
    monkeypatch.setattr("ponyflash.PonyFlash", MockPonyFlash)


@pytest.fixture
def mock_requests(monkeypatch):
    """Mock requests 模块"""
    class MockResponse:
        content = b"mock image data"
        
        def raise_for_status(self):
            pass
    
    def mock_get(*args, **kwargs):
        return MockResponse()
    
    monkeypatch.setattr("requests.get", mock_get)


class TestImageGenerator:
    """测试图片生成器"""
    
    def test_init_with_api_key(self, mock_ponyflash):
        """测试使用 API Key 初始化"""
        import sys
        sys.path.insert(0, '/tmp/postskill-fork')
        from scripts.image_generator import ImageGenerator
        
        gen = ImageGenerator(api_key="test-key")
        assert gen.api_key == "test-key"
        assert gen.client is not None
    
    def test_init_with_env_var(self, mock_ponyflash, monkeypatch):
        """测试使用环境变量初始化"""
        import sys
        sys.path.insert(0, '/tmp/postskill-fork')
        from scripts.image_generator import ImageGenerator
        
        monkeypatch.setenv("PONYFLASH_API_KEY", "env-test-key")
        gen = ImageGenerator()
        assert gen.api_key == "env-test-key"
    
    def test_init_without_api_key_raises_error(self):
        """测试缺少 API Key 时抛出错误"""
        import sys
        sys.path.insert(0, '/tmp/postskill-fork')
        from scripts.image_generator import ImageGenerator
        
        os.environ.pop("PONYFLASH_API_KEY", None)
        
        with pytest.raises(RuntimeError, match="初始化PonyFlash客户端失败"):
            ImageGenerator()
    
    def test_dry_run_mode(self):
        """测试 dry_run 模式"""
        import sys
        sys.path.insert(0, '/tmp/postskill-fork')
        from scripts.image_generator import ImageGenerator
        
        gen = ImageGenerator(dry_run=True)
        assert gen.dry_run is True
        assert gen.client is None
    
    def test_generate_with_dry_run(self):
        """测试 dry_run 模式生成"""
        import sys
        sys.path.insert(0, '/tmp/postskill-fork')
        from scripts.image_generator import ImageGenerator
        
        gen = ImageGenerator(dry_run=True)
        
        copies = [
            {"style": "干货型", "topic": "AI学习"},
            {"style": "故事型", "topic": "创业故事"},
        ]
        
        with tempfile.TemporaryDirectory() as tmpdir:
            results = gen.generate(copies, output_dir=tmpdir)
            
            assert len(results) == 2
            assert results[0]["mock"] is True
            assert results[0]["style"] == "干货型"
            assert results[1]["style"] == "故事型"
    
    def test_generate_single_image(self, mock_ponyflash, mock_requests):
        """测试单张图片生成"""
        import sys
        sys.path.insert(0, '/tmp/postskill-fork')
        from scripts.image_generator import ImageGenerator
        
        gen = ImageGenerator(api_key="test-key")
        
        copy = {"style": "干货型", "topic": "AI学习"}
        
        with tempfile.TemporaryDirectory() as tmpdir:
            result = gen._generate_single_image(copy, 0, Path(tmpdir))
            
            assert result["style"] == "干货型"
            assert result["filename"].endswith(".png")
            assert Path(result["local_path"]).parent == Path(tmpdir)
    
    def test_style_prompts_mapping(self):
        """测试风格提示词映射"""
        import sys
        sys.path.insert(0, '/tmp/postskill-fork')
        from scripts.image_generator import ImageGenerator
        
        assert "干货型" in ImageGenerator.STYLE_PROMPTS
        assert "故事型" in ImageGenerator.STYLE_PROMPTS
        assert "金句型" in ImageGenerator.STYLE_PROMPTS
        assert "modern minimalist" in ImageGenerator.STYLE_PROMPTS["干货型"]


class TestIntegrationWithoutAPI:
    """无需 API 的集成测试"""
    
    def test_full_workflow_dry_run(self):
        """测试完整 dry_run 工作流"""
        import sys
        sys.path.insert(0, '/tmp/postskill-fork')
        from scripts.image_generator import ImageGenerator
        
        gen = ImageGenerator(dry_run=True)
        
        copies = [
            {"style": "干货型", "topic": "AI醒觉社", "title": "如何学习AI"},
            {"style": "金句型", "topic": "AI醒觉社", "title": "AI改变未来"},
            {"style": "故事型", "topic": "AI醒觉社", "title": "我的AI之路"},
        ]
        
        with tempfile.TemporaryDirectory() as tmpdir:
            images = gen.generate(copies, output_dir=tmpdir)
            
            assert len(images) == 3
            for i, img in enumerate(images):
                assert img["index"] == i
                assert "style" in img
                assert "filename" in img
                assert img["mock"] is True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
