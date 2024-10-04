import java.util.List;
import uk.ac.cam.ch.wwmm.oscar.Oscar;
import uk.ac.cam.ch.wwmm.oscar.chemnamedict.entities.ResolvedNamedEntity;
import uk.ac.cam.ch.wwmm.oscar.chemnamedict.entities.ChemicalStructure;
import uk.ac.cam.ch.wwmm.oscar.chemnamedict.entities.FormatType;

public class Test {
  public static void main(String[] args) {
    String s = "Figure 5. Kinetic characteristic tests of chemical reaction between Li1–xCoO2(x= 0, 0.3, 0.5) and typical sulfide SEs. (a) DSC curves of the Li1–xCoO2+ Li6PS5Cl mixed powder at different heating rates (3, 5, 7, 15, 20 °C/min).";
    Oscar oscar = new Oscar();
    List<ResolvedNamedEntity> entities = oscar.findAndResolveNamedEntities(s);
    for (ResolvedNamedEntity ne : entities) {
      System.out.println(ne.getSurface());
      ChemicalStructure stdInchi = ne.getFirstChemicalStructure(FormatType.STD_INCHI);
      if (stdInchi != null) {
        System.out.println(stdInchi);
      }
      System.out.println();
    }
  }
}
