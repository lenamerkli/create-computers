package me.merkli.create_computers.item;

import com.simibubi.create.AllTags;
import com.simibubi.create.content.processing.sequenced.SequencedAssemblyItem;
import com.simibubi.create.foundation.data.recipe.CompatMetals;
import com.simibubi.create.foundation.item.TagDependentIngredientItem;
import com.tterrag.registrate.util.entry.ItemEntry;

import net.minecraft.tags.TagKey;
import net.minecraft.world.item.Item;

import static com.simibubi.create.AllTags.AllItemTags.CRUSHED_RAW_MATERIALS;
import static me.merkli.create_computers.CreateComputersMod.REGISTRATE;

public class AllItems {

	static {
		REGISTRATE.creativeModeTab(() -> AllCreativeModeTabs.BASE_CREATIVE_TAB);
	}

	public static final ItemEntry<Item> MILLED_SAND = ingredient("milled_sand");

	private static ItemEntry<Item> ingredient(String name) {
		return REGISTRATE.item(name, Item::new)
				.register();
	}

	private static ItemEntry<SequencedAssemblyItem> sequencedIngredient(String name) {
		return REGISTRATE.item(name, SequencedAssemblyItem::new)
				.register();
	}

	@SafeVarargs
	private static ItemEntry<Item> taggedIngredient(String name, TagKey<Item>... tags) {
		return REGISTRATE.item(name, Item::new)
				.tag(tags)
				.register();
	}

	private static ItemEntry<TagDependentIngredientItem> compatCrushedOre(CompatMetals metal) {
		String metalName = metal.getName();
		return REGISTRATE
				.item("crushed_raw_" + metalName,
						props -> new TagDependentIngredientItem(props, AllTags.forgeItemTag(metalName + "_ores")))
				.tag(CRUSHED_RAW_MATERIALS.tag)
				.register();
	}

	public static void register() {}

}
