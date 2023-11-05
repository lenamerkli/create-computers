package me.merkli.create_computers.item;

import me.merkli.create_computers.CreateComputersMod;
import net.fabricmc.fabric.api.client.itemgroup.FabricItemGroupBuilder;
import net.minecraft.item.ItemGroup;
import net.minecraft.item.ItemStack;
import net.minecraft.item.Items;
import net.minecraft.util.Identifier;

public class ModItemGroup {
	public static final ItemGroup COMPUTERS = FabricItemGroupBuilder.build(
		new Identifier(CreateComputersMod.ID, "computers"), () -> new ItemStack(Items.COMPARATOR)
	);
}
