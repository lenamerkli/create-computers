package me.merkli.create_computers.block;

import me.merkli.create_computers.CreateComputersMod;
import net.fabricmc.fabric.api.item.v1.FabricItemSettings;
import net.minecraft.block.Block;
import net.minecraft.item.BlockItem;
import net.minecraft.item.Item;
import net.minecraft.item.ItemGroup;
import net.minecraft.util.Identifier;
import net.minecraft.util.registry.Registry;


public class ModBlocks {

	private static Block registerBlock(String name, Block block, ItemGroup tab){
		registerBlockItem(name, block, tab);
		return Registry.register(Registry.BLOCK, new Identifier(CreateComputersMod.ID, name), block);
	}

	private static Item registerBlockItem(String name, Block block, ItemGroup tab){
		return Registry.register(Registry.ITEM, new Identifier(CreateComputersMod.ID, name),
				new BlockItem(block, new FabricItemSettings().group(tab)));
	}

	public static void registerModBlocks() {
		CreateComputersMod.LOGGER.debug("Registering ModBlocks for "+ CreateComputersMod.ID);
	}
}
