import { authAxios } from "$lib/features/auth/state/auth";
import { createPrototypeAtom } from "$lib/features/prototypes/atoms";
import { useSystemDiagrams, useSystemInterfaces } from "$lib/features/prototypes/queries";
import {
    Button,
    CircularProgress,
    Divider,
    FormControl,
    FormLabel,
    Input,
    Modal,
    ModalClose,
    ModalDialog,
    Switch,
    Typography
} from "@mui/joy";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import CryptoJS from 'crypto-js';
import { useAtom } from "jotai";
import React, { useEffect, useState } from "react";
import { useParams } from "react-router";
import Select from "react-select";

type PrototypeInput = {
    name: string;
    description?: string;
    system: string;
    running?: boolean;
    metadata: Record<string, any>;
    database_hash?: string;
};

type PrototypeOutput = {
    id: string;
    name: string;
    description: string;
    system: string;
    running: boolean;
};

export const CreatePrototype: React.FC = () => {
    const [open, setOpen] = useAtom(createPrototypeAtom);
    const close = () => setOpen(false);
    const { systemId } = useParams();
    const [interfaces, isSuccessInterfaces] = useSystemInterfaces(systemId);
    const [diagrams, isSuccessDiagrams] = useSystemDiagrams(systemId);
    const [selectedInterfaces, setSelectedInterfaces] = useState([]);
    const [error, setError] = useState<string | null>(null);
    const [generationError, setGenerationError] = useState<string | null>(null);
    const [useAuthentication, setUseAuthentication] = useState(true);
    const [useSyntheticData, setUseSyntheticData] = useState(false); // New state for Synthetic Data
    const [syntheticCounts, setSyntheticCounts] = useState<Record<string, number>>({}); // state to store synthetic data counts
    const [showSyntheticModal, setShowSyntheticModal] = useState(false); // modal state
    const [syntheticInstructions, setSyntheticInstructions] = useState<string>(''); // state to store custom instructions for synthetic data generation
    const [databaseHash, setDatabaseHash] = useState<string | null>(null);
    const [databasePrototypes, setDatabasePrototypes] = useState([]);
    const [selectedDatabasePrototype, setSelectedDatabasePrototype] = useState(null);
    const [globalSyntheticCount, setGlobalSyntheticCount] = useState<number | ''>(''); // New global count
    const [nodeCount, setNodeCount] = useState<number | null>(null);
    const [instructionChoice, setInstructionChoice] = useState<'global' | 'per-table' | null>(null);
    const [syntheticInstructionsPerNode, setSyntheticInstructionsPerNode] = useState<Record<string, string>>({});


    useEffect(() => {
        if (isSuccessInterfaces && interfaces) {
            setSelectedInterfaces(interfaces.map((e) => ({ label: e.name, value: e })));
        }
    }, [interfaces, isSuccessInterfaces]);

    useEffect(() => {
        const computeHash = async () => {
            if (systemId && isSuccessInterfaces) {
                const [classifiers, relations] = await Promise.all([
                    authAxios.get(`v1/metadata/systems/${systemId}/classes/`),
                    authAxios.get(`v1/metadata/systems/${systemId}/classifier-relations/`),
                ]);

                const interfaceNames = interfaces.map((e) => ({ name: e.name }));
                const inputString = `${systemId}${JSON.stringify(classifiers.data)}${JSON.stringify(relations.data)}${JSON.stringify(interfaceNames)}`;
                const hash = CryptoJS.SHA256(inputString).toString(CryptoJS.enc.Hex);
                setDatabaseHash(hash);
            }
        };

        computeHash();
    }, [systemId, interfaces, isSuccessInterfaces]);

    useEffect(() => {
        const fetchDatabasePrototypes = async () => {
            if (databaseHash) {
                try {
                    const { data } = await authAxios.get(`v1/generator/prototypes/${databaseHash}`);
                    setDatabasePrototypes(data.map((e) => ({ label: e.name, value: e })));
                } catch (error) {
                    console.error("Failed to fetch database prototypes:", error);
                }
            }
        };

        fetchDatabasePrototypes();
    }, [databaseHash]);

    const { mutateAsync, isPending } = useMutation<
        PrototypeOutput,
        unknown,
        PrototypeInput
    >({
        mutationFn: async (input) => {
            const { name, description, system, metadata } = input;
            if (selectedDatabasePrototype) {
                const { data } = await authAxios.post(`v1/generator/prototypes/?database_prototype_name=${selectedDatabasePrototype.label}`, {
                    name,
                    description,
                    system_id: system,
                    metadata,
                    database_hash: databaseHash,
                });
                return data
            }
            else {
                const { data } = await authAxios.post(`v1/generator/prototypes/?database_prototype_name=`, {
                    name,
                    description,
                    system_id: system,
                    metadata,
                    database_hash: databaseHash,
                });
                return data
            }

        },
        onError: (error) => {
            setGenerationError("An error occurred while creating the prototype!");
        },
    });

    const queryClient = useQueryClient();
    const onSubmit: React.FormEventHandler<HTMLFormElement> = async (e) => {
        e.preventDefault();
        setError(null);

        const formData = new FormData(e.currentTarget);
        const name = `${formData.get("name")}`.trim();
        const description = `${formData.get("description")}`;
        const running = Boolean(`${formData.get("running")}`);
        const metadata = {
            "diagrams": diagrams,
            "interfaces": selectedInterfaces,
            "useAuthentication": useAuthentication,
            "useSyntheticData": useSyntheticData,
            "syntheticCounts": syntheticCounts,
            "syntheticInstructions": instructionChoice === 'global' ? syntheticInstructions : '', // global instruction
            "syntheticInstructionsPerNode": instructionChoice === 'per-table' ? syntheticInstructionsPerNode : {}, // per-table instructions
        };

        const alphanumericRegex = /^[a-zA-Z0-9]+$/;
        if (!alphanumericRegex.test(name)) {
            setError("Name may only contain alphanumeric characters!");
            return;
        }

        if (!databaseHash) {
            setError("No database hash.");
            return;
        }

        mutateAsync({
            name,
            description,
            system: systemId || "",
            running,
            metadata,
            database_hash: databaseHash,
        }).then(() => {
            queryClient.invalidateQueries({ queryKey: ['prototypes', systemId] })
            close();
        }).catch((err) => {
            console.log(err)
        });
    };

    if (isPending) {
        return (
            <Modal open>
                <ModalDialog className="flex flex-row items-center gap-2">
                    <CircularProgress className="animate-spin" />
                    <Typography>
                        <h1 className="text-lg">Generating...</h1>
                    </Typography>
                </ModalDialog>
            </Modal>
        );
    }

    const hasName = (obj: any): obj is { name: string } => {
        return obj && typeof obj.name === 'string';
    };

    const extractNodeNames = (node: any) => {
        // Loop through all properties of the node (cls, enum, etc.)
        const subObjectWithName = Object.values(node).find((sub) => hasName(sub));

        return subObjectWithName ? subObjectWithName.name : null;
    };


    // Update synthetic data counts
    const updateValue = (name: string, value: number) => {
        setSyntheticCounts((prev) => ({
            ...prev,
            [name]: value, // Update the value for the specified name
        }));
    };

    const validClassNames =
        interfaces[0]?.data?.sections?.map((section) => section.class) || [];
    return (
        <>
            <Modal open={open} onClose={() => { close(); setGenerationError(null) }}>
                <ModalDialog>
                    <div className="flex w-full flex-row justify-between pb-1">
                        <div className="flex flex-col">
                            <h1 className="font-bold">Generate Prototype</h1>
                            <h3 className="text-sm">Generate a new prototype using current metadata</h3>
                        </div>
                        <ModalClose
                            sx={{ position: "relative", top: 0, right: 0 }}
                        />
                    </div>
                    <Divider />
                    <form
                        id="create-project"
                        className="max-h-[400px] overflow-y-auto pr-2"
                        onSubmit={onSubmit}
                    >
                        <FormControl required>
                            <FormLabel>Name</FormLabel>
                            <Input name="name" placeholder="Prototype" required />
                            {error && (
                                <Typography sx={{ margin: '2px' }}>
                                    <h1 className="text-sm text-red-400">{error}</h1>
                                </Typography>
                            )}
                        </FormControl>
                        <FormControl>
                            <FormLabel>Description</FormLabel>
                            <Input name="description" placeholder="A whole new world..." />
                        </FormControl>
                        <FormControl>
                            <FormLabel>Interfaces</FormLabel>
                            <Select
                                isMulti
                                name="interfaces"
                                options={interfaces.map((e) => ({ label: e.name, value: e }))}
                                value={selectedInterfaces}
                                onChange={(newValue) => setSelectedInterfaces(newValue ? newValue.map((v) => v.value) : [])}
                            />
                        </FormControl>
                        <FormControl>
                            <FormLabel>Reuse database</FormLabel>
                            <Select
                                name="database"
                                options={databasePrototypes}
                                value={selectedDatabasePrototype}
                                onChange={setSelectedDatabasePrototype}
                            />
                        </FormControl>
                        <FormControl>
                            <span className="flex flex-row items-center gap-2">
                                <Switch
                                    defaultChecked={useAuthentication}
                                    onChange={(e) => setUseAuthentication(e.target.checked)}
                                />
                                <FormLabel sx={{ marginTop: '4px' }}>Use Authentication</FormLabel>
                            </span>
                        </FormControl>
                        <FormControl>
                            <div className="flex flex-col gap-1">
                                <span className="flex flex-row items-center gap-2">
                                    <Switch
                                        checked={useSyntheticData}
                                        onChange={(e) => {
                                            const checked = e.target.checked;
                                            setUseSyntheticData(checked); // synthetic data generation button 
                                            if (checked) setShowSyntheticModal(true); // opens the new window for synthetic data
                                        }}
                                    />
                                    <FormLabel sx={{ marginTop: '4px' }}>Use Synthetic Data</FormLabel>
                                </span>
                            </div>
                        </FormControl>
                    </form>
                    <Divider />
                    <div className="flex flex-row pt-1">
                        <Button form="create-project" type="submit" disabled={isPending}>
                            {isPending ? (
                                <div className="flex flex-row gap-2">
                                    <CircularProgress className="animate-spin" />
                                    <p>Generating</p>
                                </div>
                            ) : "Create"}
                        </Button>
                    </div>
                    {generationError && (
                        <Typography sx={{ margin: '2px' }}>
                            <h1 className="text-lg text-red-800">{generationError}</h1>
                        </Typography>
                    )}
                </ModalDialog>
            </Modal>

            {/* Synthetic Data Popup Modal */}
            {/* Synthetic Data Modal (custom instruction wizard) */}
            <Modal open={showSyntheticModal} onClose={() => setShowSyntheticModal(false)}>
                <ModalDialog>
                    <Typography level="h4" className="mb-2">Synthetic Data Setup</Typography>

                    {/* Step 1: Number of Nodes */}
                    <FormControl>
                        <FormLabel>How many tables (nodes) do you want to configure?</FormLabel>
                        <Input
                            type="number"
                            min="1"
                            value={nodeCount || ''}
                            onChange={(e) => {
                                const count = parseInt(e.target.value, 10);
                                if (!isNaN(count) && count > 0) setNodeCount(count);
                                else setNodeCount(null);
                                // Reset previous instructions
                                setInstructionChoice(null);
                                setSyntheticInstructions('');
                                setSyntheticInstructionsPerNode({});
                            }}
                        />
                    </FormControl>

                    {/* Step 2: Global vs Per-Table Choice */}
                    {nodeCount && !instructionChoice && (
                        <div className="flex flex-col gap-2 mt-4">
                            <Button
                                variant="solid"
                                onClick={() => setInstructionChoice('global')}
                            >
                                Use one global instruction for all tables
                            </Button>
                            <Button
                                variant="outlined"
                                onClick={() => setInstructionChoice('per-table')}
                            >
                                Write specific instructions for each table
                            </Button>
                        </div>
                    )}

                    {/* Global Instruction */}
                    {instructionChoice === 'global' && (
                        <FormControl className="mt-4">
                            <FormLabel>Global Instruction</FormLabel>
                            <Input
                                placeholder="e.g., Generate realistic data with names"
                                value={syntheticInstructions}
                                onChange={(e) => setSyntheticInstructions(e.target.value)}
                            />
                        </FormControl>
                    )}

                    {/* Per-Table Instructions */}
                    {instructionChoice === 'per-table' && (
                        <div className="mt-4 space-y-4">
                            {[...Array(nodeCount)].map((_, i) => (
                                <FormControl key={i}>
                                    <FormLabel>Table {i + 1} Instruction</FormLabel>
                                    <Input
                                        placeholder={`Instruction for Table ${i + 1}`}
                                        value={syntheticInstructionsPerNode[`table_${i + 1}`] || ''}
                                        onChange={(e) =>
                                            setSyntheticInstructionsPerNode((prev) => ({
                                                ...prev,
                                                [`table_${i + 1}`]: e.target.value,
                                            }))
                                        }
                                    />
                                </FormControl>
                            ))}
                        </div>
                    )}

                    {/* Done Button */}
                    <div className="pt-4">
                        <Button onClick={() => setShowSyntheticModal(false)}>Done</Button>
                    </div>
                </ModalDialog>
            </Modal>

        </>
    );
};

export default CreatePrototype;
