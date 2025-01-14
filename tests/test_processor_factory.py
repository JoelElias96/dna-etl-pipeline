import pytest
from etl.processor_factory import ProcessorFactory

class TestProcessorFactory:

    def test_create_processor_json(self):
        processor = ProcessorFactory.create_processor('data.json', 'json')
        assert processor.__class__.__name__ == 'JSONProcessor'
    
    def test_create_processor_txt(self):
        processor = ProcessorFactory.create_processor('data.txt', 'txt')
        assert processor.__class__.__name__ == 'TXTProcessor'
    
    def test_create_processor_invalid(self):
        with pytest.raises(ValueError):
            ProcessorFactory.create_processor('data.csv', 'csv')
    
    def test_create_processor_invalid_case(self):
        with pytest.raises(ValueError):
            ProcessorFactory.create_processor('data.json', 'jso')
    
    def test_create_processor_invalid_case2(self):
        with pytest.raises(ValueError):
            ProcessorFactory.create_processor('data.txt', 'tx')
    
    def test_create_processor_invalid_case3(self):
        with pytest.raises(ValueError):
            ProcessorFactory.create_processor('data.txt', 'text')
    
    def test_create_processor_invalid_case4(self):
        with pytest.raises(ValueError):
            ProcessorFactory.create_processor('data.json', 'js')
