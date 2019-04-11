from AcademicTime import AcademicTime
from Student import Student
from Course import Course

if __name__ == "__main__":
    # MAT21A
    required_21A = {}
    required_21A["LMATBS1"] = True
    required_21A["LMATBS2"] = True
    required_21A["LMATAB1"] = True
    required_21A["LMATAB2"] = True
    required_21A["LAMA"] = True
    required_21A["LMOR"] = True
    required_21A["LMCOMATH"] = True
    required_21A["LMCOBIO"] = True
    quarters_offered_21A = ["Fall", "Winter", "Spring"]
    MAT21A = Course("MAT21A", None, "MAT21B", required_21A, quarters_offered_21A, "ALWAYS")
   
    # MAT21B
    required_21B = {}
    required_21B["LMATBS1"] = True
    required_21B["LMATBS2"] = True
    required_21B["LMATAB1"] = True
    required_21B["LMATAB2"] = True
    required_21B["LAMA"] = True
    required_21B["LMOR"] = True
    required_21B["LMCOMATH"] = True
    required_21B["LMCOBIO"] = True
    quarters_offered_21B = ["Fall", "Winter", "Spring"]
    MAT21B = Course("MAT21B", None, "MAT21C", required_21B, quarters_offered_21B, "ALWAYS")

    # MAT21C
    required_21C = {}
    required_21C["LMATBS1"] = True
    required_21C["LMATBS2"] = True
    required_21C["LMATAB1"] = True
    required_21C["LMATAB2"] = True
    required_21C["LAMA"] = True
    required_21C["LMOR"] = True
    required_21C["LMCOMATH"] = True
    required_21C["LMCOBIO"] = True
    quarters_offered_21C = ["Fall", "Winter", "Spring"]
    MAT21C = Course("MAT21C", None, "MAT21D", required_21C, quarters_offered_21C, "ALWAYS")

    # MAT21D
    required_21D = {}
    required_21D["LMATBS1"] = True
    required_21D["LMATBS2"] = True
    required_21D["LMATAB1"] = True
    required_21D["LMATAB2"] = True
    required_21D["LAMA"] = True
    required_21D["LMOR"] = True
    required_21D["LMCOMATH"] = True
    required_21D["LMCOBIO"] = True
    quarters_offered_21D = ["Fall", "Winter", "Spring"]
    MAT21D = Course("MAT21D", None, None, required_21D, quarters_offered_21D, "ALWAYS")

    # MAT22A
    required_22A = {}
    required_22A["LMATBS1"] = True
    required_22A["LMATBS2"] = True
    required_22A["LMATAB1"] = True
    required_22A["LMATAB2"] = True
    required_22A["LAMA"] = True
    required_22A["LMOR"] = True
    required_22A["LMCOMATH"] = True
    required_22A["LMCOBIO"] = True
    quarters_offered_22A = ["Fall", "Winter", "Spring"]
    MAT22A = Course("MAT22A", None, None, required_22A, quarters_offered_22A, "ALWAYS")

    # MAT22AL
    required_22AL = {}
    required_22AL["LMATBS1"] = False
    required_22AL["LMATBS2"] = False
    required_22AL["LMATAB1"] = False
    required_22AL["LMATAB2"] = False
    required_22AL["LAMA"] = False
    required_22AL["LMOR"] = False
    required_22AL["LMCOMATH"] = False
    required_22AL["LMCOBIO"] = False
    quarters_offered_22AL = ["Fall", "Winter", "Spring"]
    MAT22AL = Course("MAT22AL", None, None, required_22AL, quarters_offered_22AL, "ALWAYS")

    # ENG06
    required_ENG06 = {}
    required_ENG06["LMATBS1"] = True
    required_ENG06["LMATBS2"] = True
    required_ENG06["LMATAB1"] = True
    required_ENG06["LMATAB2"] = True
    required_ENG06["LAMA"] = True
    required_ENG06["LMOR"] = True
    required_ENG06["LMCOMATH"] = True
    required_ENG06["LMCOBIO"] = True
    quarters_offered_ENG06 = ["Fall", "Winter", "Spring"]
    ENG06 = Course("ENG06", None, None, required_ENG06, quarters_offered_ENG06, "ALWAYS")

    # MAT67
    required_67 = {}
    required_67["LMATBS1"] = False
    required_67["LMATBS2"] = False
    required_67["LMATAB1"] = False
    required_67["LMATAB2"] = False
    required_67["LAMA"] = False
    required_67["LMOR"] = False
    required_67["LMCOMATH"] = False
    required_67["LMCOBIO"] = False
    quarters_offered_67 = ["Winter"]
    MAT67 = Course("MAT67", None, None, required_67, quarters_offered_67, "ALWAYS")

    # MAT22B
    required_22B = {}
    required_22B["LMATBS1"] = True
    required_22B["LMATBS2"] = True
    required_22B["LMATAB1"] = True
    required_22B["LMATAB2"] = True
    required_22B["LAMA"] = True
    required_22B["LMOR"] = True
    required_22B["LMCOMATH"] = True
    required_22B["LMCOBIO"] = True
    quarters_offered_22B = ["Fall", "Winter", "Spring"]
    MAT22B = Course("MAT22B", None, None, required_22B, quarters_offered_22B, "ALWAYS")

    # MAT108
    required_108 = {}
    required_108["LMATBS1"] = True
    required_108["LMATBS2"] = True
    required_108["LMATAB1"] = True
    required_108["LMATAB2"] = True
    required_108["LAMA"] = True
    required_108["LMOR"] = True
    required_108["LMCOMATH"] = True
    required_108["LMCOBIO"] = True
    quarters_offered_108 = ["Fall", "Winter", "Spring"]
    MAT108 = Course("MAT108", None, "MAT127A", required_108, quarters_offered_108, "ALWAYS")

    # MAT111
    required_111 = {}
    required_111["LMATBS1"] = False
    required_111["LMATBS2"] = True
    required_111["LMATAB1"] = False
    required_111["LMATAB2"] = True
    required_111["LAMA"] = False
    required_111["LMOR"] = False
    required_111["LMCOMATH"] = False
    required_111["LMCOBIO"] = False
    quarters_offered_111 = ["Winter"]
    interests_111 = ["Teaching"]
    MAT111 = Course("MAT111", interests_111, None, required_111, quarters_offered_111, "ALWAYS")

    # MAT114
    required_114 = {}
    required_114["LMATBS1"] = False
    required_114["LMATBS2"] = False
    required_114["LMATAB1"] = False
    required_114["LMATAB2"] = False
    required_114["LAMA"] = False
    required_114["LMOR"] = False
    required_114["LMCOMATH"] = False
    required_114["LMCOBIO"] = False
    quarters_offered_114 = ["Winter"]
    interests_114 = ["Geometry"]
    MAT114 = Course("MAT114", interests_114, None, required_114, quarters_offered_114, "EVENALTERNATE")

    # MAT115A
    required_115A = {}
    required_115A["LMATBS1"] = False
    required_115A["LMATBS2"] = True
    required_115A["LMATAB1"] = False
    required_115A["LMATAB2"] = True
    required_115A["LAMA"] = False
    required_115A["LMOR"] = False
    required_115A["LMCOMATH"] = False
    required_115A["LMCOBIO"] = False
    quarters_offered_115A = ["Fall"]
    interests_115A = ["Teaching"]
    MAT115A = Course("MAT115A", interests_115A, "MAT115B", required_115A, quarters_offered_115A, "ALWAYS")

    # MAT115B
    required_115B = {}
    required_115B["LMATBS1"] = False
    required_115B["LMATBS2"] = False
    required_115B["LMATAB1"] = False
    required_115B["LMATAB2"] = False
    required_115B["LAMA"] = False
    required_115B["LMOR"] = False
    required_115B["LMCOMATH"] = False
    required_115B["LMCOBIO"] = False
    quarters_offered_115B = ["Winter"]
    interests_115B = ["Teaching"]
    MAT115B = Course("MAT115B", interests_115B, None, required_115B, quarters_offered_115B, "EVENALTERNATE")





    

