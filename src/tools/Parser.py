import math
import xml.etree.ElementTree as ET

class MetricsParser:

    """XML Parser class to extract metrics data from an ontology

    This class responsability lies on parsing an xml file which holds all the metrics
    generated by the OQuaRE library. This class provides functionality to extract
    certain metrics from a given file.

    """

    def __init__(self, metrics_file: str):
        """MetricsParser init method

        Stores as fields the XML tree aswell as the root node of said tree.
        This allows for easy XML file parsing on its class methods

        Keyword arguments:
        metrics_file -- Path to xml file which holds the generated metrics of a given ontology
        """
        self.tree = ET.parse(metrics_file)
        self.root = self.tree.getroot()

    def parse_oquare_value(self) -> float:
        """OQuaRE model value parse method
        
        Returns a float value which represents the oquare model metric value

        """
        oquare_value = math.floor(float(self.root.find('oquareModel').attrib.get('oquareValue')) * 10 ** 2) / 10 ** 2  
        return oquare_value
    
    def parse_scaled_metrics(self) -> dict:
        """OQuaRE scaled metrics parse method
        
        Returns a dictionary which holds the scaled value for each OQuaRE metric

        """
        scaled_metrics = self.root.findall('./oquareMetricsScaled/')
        metrics_dict = {}
        for metric in scaled_metrics:
            metrics_dict[metric.tag] = math.floor(float(metric.text) * 10 ** 2) / 10 ** 2  
        
        return metrics_dict
    
    def parse_metrics(self):
        """OQuaRE metrics parse method
        
        Returns a dictionary which holds the value for each OQuaRE metric

        """
        metrics = self.root.findall('./oquareMetrics/')
        metrics_dict = {}
        for metric in metrics:
            metrics_dict[metric.tag] = math.floor(float(metric.text) * 10 ** 2) / 10 ** 2   

        return metrics_dict

    def parse_characteristics_metrics(self):
        """OQuaRE characteristics parse method
        
        Returns a dictionary which holds the values aswell as the subcharacteristics and their values
        of each characteristic.

        The dictionary is structured as it follows
        characteristic:
            value: float
            subcharacteristics
                subcharacteristics: float

        """
        oquare_model = self.root.findall('oquareModel/')
        oquare_model_dict = {}
        for characteristic in oquare_model:
            characteristic_name, characteristic_value = next(iter(characteristic.attrib.items()))

            oquare_characteristic = {}
            oquare_characteristic['value'] = math.floor(float(characteristic_value) * 10 ** 2) / 10 ** 2  
            
            oquare_sub_characteristics = {}
            
            # Get subcharacteristics
            subcharacteristics = self.root.findall('oquareModel/' + characteristic.tag + '/')
            for subcharacteristic in subcharacteristics:
                oquare_sub_characteristics[subcharacteristic.tag] = math.floor(float(subcharacteristic.text) * 10 ** 2) / 10 ** 2  

            # Put subcharacteristics under the main characteristics
            oquare_characteristic['subcharacteristics'] = oquare_sub_characteristics

            # Put each characteristics inside the oquare_model_dict
            oquare_model_dict[characteristic_name] = oquare_characteristic

        return oquare_model_dict
