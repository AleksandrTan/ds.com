class SetBarcode:

    def __init__(self, pre_barcode):
        self.pre_data = '2000000'
        self.pre_barcode = pre_barcode

    def generate_barcode(self):
        return self.pre_data + self.pre_barcode + self.generate_control_num()

    def generate_control_num(self):
        barcode = self.pre_data + self.pre_barcode
        s1 = sum([int(item) for (i, item) in enumerate(barcode) if i % 2 == 0])
        s2 = sum([int(item) for (i, item) in enumerate(barcode) if i % 2 != 0]) * 3
        s3 = s1 + s2
        if s3 % 10:
            s4 = s3
            res = 0
            while s4 % 10:
                s4 = s4 + 1
                res = s4
        else:
            res = s3

        return str(res - s3)