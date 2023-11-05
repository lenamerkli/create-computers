package me.merkli.create_computers.item;

import me.merkli.create_computers.CreateComputersMod;
import net.fabricmc.fabric.api.item.v1.FabricItemSettings;
import net.minecraft.item.Item;
import net.minecraft.util.Identifier;
import net.minecraft.util.registry.Registry;

public class ModItems {

	private static final Item MILLED_SAND = registerItem("milled_sand",
			new Item(new FabricItemSettings().group(ModItemGroup.COMPUTERS)));

	private static Item registerItem(String name, Item item){
		return Registry.register(Registry.ITEM, new Identifier(CreateComputersMod.ID, name), item);
	}

	public static void registerModItems(){
		CreateComputersMod.LOGGER.debug("Registering Mod Items for " + CreateComputersMod.ID);
	}

}
