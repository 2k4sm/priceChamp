import scrappy as sp

class test_scrappy:
    """
    contains test suite to test scrappy.
    """
    
    def __init__(self,pnames):
        
        self.pnames = pnames
    
    def test_status(self):
        """
        Checks for the status codes after making an request.If tests fails prints the failing website name with the status code.
        """
        for p in self.pnames:
            prod = sp.Product(p)
            status_codes = sp.Request(prod).make_request()["status"]
            tcount = 1;
            for stat in status_codes:
                if (status_codes[stat] != 200):
                    print(f"Test case {tcount} Failed.")
                    print(f" {stat} responded with {status_codes[stat]} status.")
                    break;
                else:
                    print(f"Test case {tcount} passed.")
                    tcount+=1
            print(f"Tests Done for Product {p}.")
   
   
# driver code.
if __name__ == "__main__":
    pnames = ["iphone 13","samsung s23","woben water bottle","redmi 12 5g","one plus 9r","sony headphones","poco m6 pro 5g"]
    tc1 = test_scrappy(pnames)

    tc1.test_status()
        
        