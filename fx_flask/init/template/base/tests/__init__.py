"""生成测试结果报告"""
import pytest

pytest.main([
    '--report=_report.html', '--title=报告标题', '--tester=测试员', '--desc=报告描述信息', '--template=2', '--cov-report=html',
    '--cov'
])
