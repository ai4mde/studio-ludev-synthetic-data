import { authAxios } from "$lib/features/auth/state/auth";
import { useQuery } from "@tanstack/react-query";
import { useAtom } from "jotai";
import { Plus } from "lucide-react";
import React from "react";
import { createSystemAtom } from "../../atoms";
import CreateSystem from "./CreateSystem";

type SystemOut = {
    id: string;
    name: string;
    description?: string;
};

type Props = {
    project: string;
};

export const ListSystem: React.FC<Props> = ({ project }) => {
    const { data, isSuccess } = useQuery<SystemOut[]>({
        queryKey: ["systems", `${project}`],
        queryFn: async () => {
            return (
                await authAxios.get(`/v1/metadata/systems/`, {
                    params: {
                        project: project,
                    },
                })
            ).data;
        },
        enabled: !!project,
    });

    const [, setCreate] = useAtom(createSystemAtom);

    return (
        <>
            <CreateSystem project={project} />
            {isSuccess &&
                data.map((e) => (
                    <a
                        href={`/systems/${e.id}`}
                        className="flex h-fit w-48 flex-col gap-2 overflow-hidden text-ellipsis rounded-md bg-stone-200 p-4 hover:bg-stone-300"
                    >
                        <h3 className="text-xl font-bold">{e.name}</h3>
                        <h3 className="text-sm">{e.description}</h3>
                        <span className="pt-2 text-right text-xs text-stone-500">
                            {e.id.split("-").slice(-1)}
                        </span>
                    </a>
                ))}
            <button
                onClick={() => setCreate(true)}
                className="h-fill flex flex-col items-center justify-center gap-2 rounded-md bg-stone-100 p-4 hover:bg-stone-200"
            >
                <Plus />
            </button>
        </>
    );
};

export default ListSystem;
