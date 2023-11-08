package me.merkli.create_computers.item;

import net.minecraft.world.item.ItemStack;

import org.jetbrains.annotations.NotNull;

public class BaseCreativeModeTab extends CreateComputersCreativeModeTab {
	public BaseCreativeModeTab() {
		super("computers");
	}

	@Override
	public @NotNull ItemStack makeIcon() {
		return AllItems.MILLED_SAND.asStack();
	}
}
