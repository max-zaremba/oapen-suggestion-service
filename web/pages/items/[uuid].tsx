import type { GetStaticProps, GetStaticPaths } from "next";
import { OAPENItems } from "../../lib/oapen";
import type { OAPENItemWithMetadata } from "../../lib/oapen/OAPENTypes";
import { RenderItem } from "../../components/render/RenderItem";

interface SingleItemProps {
  item: OAPENItemWithMetadata;
}

export default function ItemSingle({ item }: SingleItemProps) {
  const name =
    item.name || item.metadata.find(({ key }) => key == "grantor.name")?.value;
  const type = item.metadata.find(({ key }) => key == "dc.type")?.value;
  console.log({ item });
  return (
    <>
      <RenderItem item={item} />
    </>
  );
}

// TODO update
export const getStaticPaths: GetStaticPaths = async () => {
  return {
    paths: [],
    fallback: "blocking", // can also be true or 'blocking
  };
};

export const getStaticProps: GetStaticProps<SingleItemProps> = async (
  context
) => {
  const item = await OAPENItems.getItemWithMetadata(context?.params?.uuid + "");
  const data: SingleItemProps = {
    item,
  };

  return {
    props: {
      ...data,
    },
  };
};
